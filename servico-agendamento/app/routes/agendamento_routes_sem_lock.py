"""
Rotas para gerenciamento de agendamentos SEM LOCK
ENTREGA 2: Demonstra o PROBLEMA da condição de corrida
⚠️ VERSÃO DIDÁTICA - NÃO usar em produção!
"""
from flask import jsonify, request, url_for, current_app
from app.routes import agendamentos_bp
from app.models.agendamento import Agendamento
from app.models.cientista import Cientista
from app import db
from app.utils.logger import log_audit
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@agendamentos_bp.route('/agendamentos', methods=['GET'])
def list_agendamentos():
    """GET /api/v1/agendamentos - Lista agendamentos com filtros e paginação"""
    logger.info("Listando agendamentos")
    
    # Parâmetros
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    per_page = min(per_page, 100)
    
    # Filtros
    cientista_id = request.args.get('cientista_id', type=int)
    status = request.args.get('status')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    # Query base
    query = Agendamento.query
    
    if cientista_id:
        query = query.filter_by(cientista_id=cientista_id)
    
    if status:
        query = query.filter_by(status=status)
    
    if data_inicio:
        try:
            dt_inicio = datetime.fromisoformat(data_inicio.replace('Z', '+00:00'))
            query = query.filter(Agendamento.horario_inicio_utc >= dt_inicio)
        except ValueError:
            return jsonify({'error': 'data_inicio inválida'}), 400
    
    if data_fim:
        try:
            dt_fim = datetime.fromisoformat(data_fim.replace('Z', '+00:00'))
            query = query.filter(Agendamento.horario_fim_utc <= dt_fim)
        except ValueError:
            return jsonify({'error': 'data_fim inválida'}), 400
    
    # Ordenar por data
    query = query.order_by(Agendamento.horario_inicio_utc.asc())
    
    # Paginar
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    agendamentos = [a.to_dict() for a in pagination.items]
    
    response = {
        'agendamentos': agendamentos,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total_items': pagination.total,
            'total_pages': pagination.pages
        },
        '_links': {
            'self': {'href': url_for('agendamentos.list_agendamentos', page=page, _external=True)}
        }
    }
    
    return jsonify(response), 200

@agendamentos_bp.route('/agendamentos', methods=['POST'])
def create_agendamento():
    """
    POST /api/v1/agendamentos
    Cria um novo agendamento SEM LOCK (Entrega 2 - Demonstração do problema)
    
    ⚠️ ATENÇÃO: Esta versão NÃO usa o serviço coordenador!
    Permite múltiplos agendamentos simultâneos no mesmo horário (condição de corrida)
    """
    logger.info("Criando novo agendamento (MODO SEM LOCK)")
    logger.warning("⚠️ Sistema rodando SEM proteção de lock! Condição de corrida possível!")
    
    data = request.get_json()
    
    # Validar dados
    config = {
        'DURACAO_MINIMA_MINUTOS': current_app.config['DURACAO_MINIMA_MINUTOS'],
        'DURACAO_MAXIMA_MINUTOS': current_app.config['DURACAO_MAXIMA_MINUTOS'],
        'ANTECEDENCIA_MINIMA_HORAS': current_app.config['ANTECEDENCIA_MINIMA_HORAS']
    }
    
    errors = Agendamento.validate_data(data, config)
    if errors:
        logger.warning(f"Dados inválidos: {errors}")
        return jsonify({'error': 'Dados inválidos', 'details': errors}), 400
    
    # Verificar se cientista existe e está ativo
    cientista = Cientista.query.get(data['cientista_id'])
    if not cientista:
        logger.warning(f"Cientista ID {data['cientista_id']} não encontrado")
        return jsonify({'error': 'Cientista não encontrado'}), 404
    
    if not cientista.ativo:
        logger.warning(f"Cientista ID {data['cientista_id']} está inativo")
        return jsonify({'error': 'Cientista inativo não pode agendar'}), 422
    
    # Converter datas
    inicio = datetime.fromisoformat(data['horario_inicio_utc'].replace('Z', '+00:00'))
    fim = datetime.fromisoformat(data['horario_fim_utc'].replace('Z', '+00:00'))
    
    # ⚠️ SEM LOCK - Apenas verificação no banco (não atômica!)
    logger.info("Iniciando verificação de conflito no BD (SEM LOCK - UNSAFE!)")
    
    conflitos = Agendamento.check_conflicts(inicio, fim)
    
    if conflitos:
        logger.warning(f"Conflito de horário detectado com agendamento(s): {[c.id for c in conflitos]}")
        log_audit('AGENDAMENTO_CONFLITO', {
            'cientista_id': cientista.id,
            'horario_inicio_utc': inicio.isoformat() + 'Z',
            'conflitos_com': [c.id for c in conflitos]
        })
        return jsonify({
            'error': 'Conflito de horário',
            'conflitos': [c.to_dict(include_links=False) for c in conflitos]
        }), 409
    
    # Verificar limite de agendamentos ativos do cientista
    agendamentos_ativos = Agendamento.query.filter_by(
        cientista_id=cientista.id,
        status='AGENDADO'
    ).count()
    
    if agendamentos_ativos >= current_app.config['MAX_AGENDAMENTOS_ATIVOS_POR_CIENTISTA']:
        logger.warning(f"Cientista {cientista.id} atingiu limite de agendamentos ativos")
        return jsonify({
            'error': f'Limite de {current_app.config["MAX_AGENDAMENTOS_ATIVOS_POR_CIENTISTA"]} agendamentos ativos atingido'
        }), 422
    
    # ⚠️ PONTO CRÍTICO: Aqui pode ocorrer race condition!
    # Entre a verificação acima e o INSERT abaixo, outra thread pode criar agendamento
    logger.warning("⚠️ RACE CONDITION WINDOW: Entre verificação e INSERT")
    
    # Criar agendamento
    logger.info("Salvando novo agendamento no BD")
    
    agendamento = Agendamento(
        cientista_id=cientista.id,
        horario_inicio_utc=inicio,
        horario_fim_utc=fim,
        objeto_celeste=data['objeto_celeste'].strip(),
        observacoes=data.get('observacoes', '').strip() or None
    )
    
    db.session.add(agendamento)
    db.session.commit()
    
    logger.info(f"Agendamento criado com ID {agendamento.id}")
    
    # Log de auditoria
    log_audit('AGENDAMENTO_CRIADO', {
        'agendamento_id': agendamento.id,
        'cientista_id': cientista.id,
        'cientista_nome': cientista.nome,
        'horario_inicio_utc': agendamento.horario_inicio_utc.isoformat() + 'Z',
        'horario_fim_utc': agendamento.horario_fim_utc.isoformat() + 'Z',
        'objeto_celeste': agendamento.objeto_celeste,
        'modo': 'SEM_LOCK'  # Indicador para análise
    })
    
    return jsonify(agendamento.to_dict()), 201

@agendamentos_bp.route('/agendamentos/<int:id>', methods=['GET'])
def get_agendamento(id):
    """GET /api/v1/agendamentos/{id} - Obtém detalhes de um agendamento"""
    logger.info(f"Buscando agendamento ID {id}")
    
    agendamento = Agendamento.query.get(id)
    
    if not agendamento:
        logger.warning(f"Agendamento ID {id} não encontrado")
        return jsonify({'error': 'Agendamento não encontrado'}), 404
    
    return jsonify(agendamento.to_dict()), 200

@agendamentos_bp.route('/agendamentos/<int:id>', methods=['DELETE'])
def cancel_agendamento(id):
    """DELETE /api/v1/agendamentos/{id} - Cancela um agendamento"""
    logger.info(f"Cancelando agendamento ID {id}")
    
    agendamento = Agendamento.query.get(id)
    
    if not agendamento:
        logger.warning(f"Agendamento ID {id} não encontrado")
        return jsonify({'error': 'Agendamento não encontrado'}), 404
    
    if agendamento.status != 'AGENDADO':
        logger.warning(f"Agendamento ID {id} não pode ser cancelado (status: {agendamento.status})")
        return jsonify({'error': f'Agendamento com status {agendamento.status} não pode ser cancelado'}), 422
    
    # Obter motivo do cancelamento (opcional)
    data = request.get_json() or {}
    motivo = data.get('motivo', 'Cancelado pelo usuário')
    
    # Atualizar agendamento
    agendamento.status = 'CANCELADO'
    agendamento.data_cancelamento = datetime.utcnow()
    agendamento.motivo_cancelamento = motivo
    
    db.session.commit()
    
    logger.info(f"Agendamento ID {id} cancelado")
    
    # Log de auditoria
    log_audit('AGENDAMENTO_CANCELADO', {
        'agendamento_id': agendamento.id,
        'cientista_id': agendamento.cientista_id,
        'cientista_nome': agendamento.cientista.nome,
        'horario_inicio_utc': agendamento.horario_inicio_utc.isoformat() + 'Z',
        'motivo': motivo
    })
    
    return jsonify(agendamento.to_dict()), 200
