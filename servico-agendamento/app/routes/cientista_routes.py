"""
Rotas para gerenciamento de cientistas
"""
from flask import jsonify, request, url_for
from app.routes import cientistas_bp
from app.models.cientista import Cientista
from app import db
from app.utils.logger import log_audit
import logging

logger = logging.getLogger(__name__)

@cientistas_bp.route('/cientistas', methods=['GET'])
def list_cientistas():
    """GET /api/v1/cientistas - Lista todos os cientistas com paginação"""
    logger.info("Listando cientistas")
    
    # Parâmetros de paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    per_page = min(per_page, 100)  # Máximo 100 por página
    
    # Filtro opcional por status
    ativo = request.args.get('ativo', type=lambda v: v.lower() == 'true')
    
    # Query base
    query = Cientista.query
    
    if ativo is not None:
        query = query.filter_by(ativo=ativo)
    
    # Paginar
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    cientistas = [c.to_dict() for c in pagination.items]
    
    response = {
        'cientistas': cientistas,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total_items': pagination.total,
            'total_pages': pagination.pages
        },
        '_links': {
            'self': {'href': url_for('cientistas.list_cientistas', page=page, per_page=per_page, _external=True)}
        }
    }
    
    # Links de navegação
    if pagination.has_prev:
        response['_links']['prev'] = {
            'href': url_for('cientistas.list_cientistas', page=page-1, per_page=per_page, _external=True)
        }
    
    if pagination.has_next:
        response['_links']['next'] = {
            'href': url_for('cientistas.list_cientistas', page=page+1, per_page=per_page, _external=True)
        }
    
    response['_links']['first'] = {
        'href': url_for('cientistas.list_cientistas', page=1, per_page=per_page, _external=True)
    }
    response['_links']['last'] = {
        'href': url_for('cientistas.list_cientistas', page=pagination.pages, per_page=per_page, _external=True)
    }
    
    logger.info(f"Retornando {len(cientistas)} cientistas (página {page}/{pagination.pages})")
    
    return jsonify(response), 200

@cientistas_bp.route('/cientistas', methods=['POST'])
def create_cientista():
    """POST /api/v1/cientistas - Cria um novo cientista"""
    logger.info("Criando novo cientista")
    
    data = request.get_json()
    
    # Validar dados
    errors = Cientista.validate_data(data)
    if errors:
        logger.warning(f"Dados inválidos: {errors}")
        return jsonify({'error': 'Dados inválidos', 'details': errors}), 400
    
    # Verificar email duplicado
    if Cientista.query.filter_by(email=data['email']).first():
        logger.warning(f"Email já cadastrado: {data['email']}")
        return jsonify({'error': 'Email já cadastrado'}), 409
    
    # Criar cientista
    cientista = Cientista(
        nome=data['nome'].strip(),
        email=data['email'].strip().lower(),
        instituicao=data['instituicao'].strip(),
        pais=data['pais'].strip(),
        especialidade=data.get('especialidade', '').strip() or None
    )
    
    db.session.add(cientista)
    db.session.commit()
    
    logger.info(f"Cientista criado com ID {cientista.id}")
    
    # Log de auditoria
    log_audit('CIENTISTA_CRIADO', {
        'cientista_id': cientista.id,
        'nome': cientista.nome,
        'email': cientista.email,
        'instituicao': cientista.instituicao
    })
    
    return jsonify(cientista.to_dict()), 201

@cientistas_bp.route('/cientistas/<int:id>', methods=['GET'])
def get_cientista(id):
    """GET /api/v1/cientistas/{id} - Obtém detalhes de um cientista"""
    logger.info(f"Buscando cientista ID {id}")
    
    cientista = Cientista.query.get(id)
    
    if not cientista:
        logger.warning(f"Cientista ID {id} não encontrado")
        return jsonify({'error': 'Cientista não encontrado'}), 404
    
    return jsonify(cientista.to_dict()), 200

@cientistas_bp.route('/cientistas/<int:id>/agendamentos', methods=['GET'])
def get_cientista_agendamentos(id):
    """GET /api/v1/cientistas/{id}/agendamentos - Lista agendamentos de um cientista"""
    logger.info(f"Listando agendamentos do cientista ID {id}")
    
    cientista = Cientista.query.get(id)
    
    if not cientista:
        logger.warning(f"Cientista ID {id} não encontrado")
        return jsonify({'error': 'Cientista não encontrado'}), 404
    
    # Filtro opcional por status
    status = request.args.get('status')
    
    query = cientista.agendamentos
    if status:
        query = query.filter_by(status=status)
    
    agendamentos = [a.to_dict() for a in query.all()]
    
    response = {
        'cientista_id': id,
        'cientista_nome': cientista.nome,
        'agendamentos': agendamentos,
        'total': len(agendamentos),
        '_links': {
            'self': {'href': url_for('cientistas.get_cientista_agendamentos', id=id, _external=True)},
            'cientista': {'href': url_for('cientistas.get_cientista', id=id, _external=True)}
        }
    }
    
    return jsonify(response), 200
