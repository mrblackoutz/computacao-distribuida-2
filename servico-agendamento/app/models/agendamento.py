"""
Modelo Agendamento
"""
from app import db
from datetime import datetime, timedelta, timezone
from sqlalchemy import Index, CheckConstraint

class Agendamento(db.Model):
    """Modelo de Agendamento"""
    __tablename__ = 'agendamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    cientista_id = db.Column(db.Integer, db.ForeignKey('cientistas.id'), nullable=False)
    horario_inicio_utc = db.Column(db.DateTime, nullable=False)
    horario_fim_utc = db.Column(db.DateTime, nullable=False)
    objeto_celeste = db.Column(db.String(300), nullable=False)
    observacoes = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False, default='AGENDADO')
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data_cancelamento = db.Column(db.DateTime)
    motivo_cancelamento = db.Column(db.Text)
    
    # Relacionamento
    cientista = db.relationship('Cientista', back_populates='agendamentos')
    
    # Índices
    __table_args__ = (
        Index('idx_horario_status', 'horario_inicio_utc', 'horario_fim_utc', 'status'),
        Index('idx_cientista', 'cientista_id'),
        Index('idx_status', 'status'),
        CheckConstraint('horario_fim_utc > horario_inicio_utc', name='check_horarios'),
        CheckConstraint("status IN ('AGENDADO', 'CANCELADO', 'CONCLUIDO')", name='check_status'),
    )
    
    def __repr__(self):
        return f'<Agendamento {self.id} - {self.objeto_celeste}>'
    
    def to_dict(self, include_links=True):
        """Serializa o objeto para dicionário"""
        data = {
            'id': self.id,
            'cientista_id': self.cientista_id,
            'cientista_nome': self.cientista.nome,
            'horario_inicio_utc': self.horario_inicio_utc.isoformat() + 'Z',
            'horario_fim_utc': self.horario_fim_utc.isoformat() + 'Z',
            'objeto_celeste': self.objeto_celeste,
            'observacoes': self.observacoes,
            'status': self.status,
            'data_criacao': self.data_criacao.isoformat() + 'Z'
        }
        
        if self.status == 'CANCELADO':
            data['data_cancelamento'] = self.data_cancelamento.isoformat() + 'Z' if self.data_cancelamento else None
            data['motivo_cancelamento'] = self.motivo_cancelamento
        
        if include_links:
            data['_links'] = self.get_links()
        
        return data
    
    def get_links(self):
        """Retorna links HATEOAS"""
        from flask import url_for
        links = {
            'self': {'href': url_for('agendamentos.get_agendamento', id=self.id, _external=True)},
            'cientista': {'href': url_for('cientistas.get_cientista', id=self.cientista_id, _external=True)}
        }
        
        # Link condicional baseado no status
        if self.status == 'AGENDADO':
            links['cancelar'] = {
                'href': url_for('agendamentos.cancel_agendamento', id=self.id, _external=True),
                'method': 'DELETE'
            }
        
        return links
    
    @staticmethod
    def validate_data(data, config):
        """Valida os dados do agendamento"""
        errors = []
        
        # Validações básicas
        if 'cientista_id' not in data:
            errors.append('cientista_id é obrigatório')
        
        if 'horario_inicio_utc' not in data:
            errors.append('horario_inicio_utc é obrigatório')
        
        if 'horario_fim_utc' not in data:
            errors.append('horario_fim_utc é obrigatório')
        
        if 'objeto_celeste' not in data:
            errors.append('objeto_celeste é obrigatório')
        
        if errors:
            return errors
        
        # Converter strings para datetime
        try:
            inicio = datetime.fromisoformat(data['horario_inicio_utc'].replace('Z', '+00:00'))
            fim = datetime.fromisoformat(data['horario_fim_utc'].replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            errors.append('Formato de data/hora inválido. Use ISO8601 (ex: 2025-12-01T03:00:00Z)')
            return errors
        
        agora = datetime.now(timezone.utc)
        
        # Validar horários
        if fim <= inicio:
            errors.append('horario_fim_utc deve ser posterior a horario_inicio_utc')
        
        duracao_minutos = (fim - inicio).total_seconds() / 60
        
        if duracao_minutos < config['DURACAO_MINIMA_MINUTOS']:
            errors.append(f'Duração mínima: {config["DURACAO_MINIMA_MINUTOS"]} minutos')
        
        if duracao_minutos > config['DURACAO_MAXIMA_MINUTOS']:
            errors.append(f'Duração máxima: {config["DURACAO_MAXIMA_MINUTOS"]} minutos')
        
        # Verificar múltiplos de 5 minutos (REQUISITO DO PROFESSOR)
        if inicio.minute % 5 != 0 or fim.minute % 5 != 0:
            errors.append('Horários devem ser múltiplos de 5 minutos (ex: 14:00, 14:05, 14:10...)')
        
        # Verificar se não é no passado
        if inicio <= agora:
            errors.append('Não é possível agendar no passado')
        
        # Verificar antecedência mínima
        antecedencia = inicio - agora
        if antecedencia < timedelta(hours=config['ANTECEDENCIA_MINIMA_HORAS']):
            errors.append(f'Antecedência mínima: {config["ANTECEDENCIA_MINIMA_HORAS"]} horas')
        
        return errors
    
    @staticmethod
    def check_conflicts(inicio, fim, cientista_id=None, agendamento_id=None):
        """Verifica conflitos de horário"""
        query = Agendamento.query.filter(
            Agendamento.status == 'AGENDADO',
            Agendamento.horario_inicio_utc < fim,
            Agendamento.horario_fim_utc > inicio
        )
        
        if agendamento_id:
            query = query.filter(Agendamento.id != agendamento_id)
        
        conflitos = query.all()
        return conflitos
