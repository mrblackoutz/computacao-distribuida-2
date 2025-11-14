"""
Modelo Cientista
"""
from app import db
from datetime import datetime
from sqlalchemy import Index

class Cientista(db.Model):
    """Modelo de Cientista"""
    __tablename__ = 'cientistas'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    instituicao = db.Column(db.String(300), nullable=False)
    pais = db.Column(db.String(100), nullable=False)
    especialidade = db.Column(db.String(200))
    data_cadastro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    
    # Relacionamento
    agendamentos = db.relationship('Agendamento', back_populates='cientista', lazy='dynamic')
    
    # Índices
    __table_args__ = (
        Index('idx_email', 'email'),
        Index('idx_ativo', 'ativo'),
    )
    
    def __repr__(self):
        return f'<Cientista {self.nome}>'
    
    def to_dict(self, include_links=True):
        """Serializa o objeto para dicionário"""
        data = {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'instituicao': self.instituicao,
            'pais': self.pais,
            'especialidade': self.especialidade,
            'ativo': self.ativo,
            'data_cadastro': self.data_cadastro.isoformat() + 'Z'
        }
        
        if include_links:
            data['_links'] = self.get_links()
        
        return data
    
    def get_links(self):
        """Retorna links HATEOAS"""
        from flask import url_for
        return {
            'self': {'href': url_for('cientistas.get_cientista', id=self.id, _external=True)},
            'agendamentos': {'href': url_for('cientistas.get_cientista_agendamentos', id=self.id, _external=True)},
            'criar_agendamento': {
                'href': url_for('agendamentos.create_agendamento', _external=True),
                'method': 'POST'
            }
        }
    
    @staticmethod
    def validate_data(data, is_update=False):
        """Valida os dados do cientista"""
        errors = []
        
        if not is_update or 'nome' in data:
            nome = data.get('nome', '').strip()
            if not nome:
                errors.append('Nome é obrigatório')
            elif len(nome) < 3:
                errors.append('Nome deve ter no mínimo 3 caracteres')
        
        if not is_update or 'email' in data:
            email = data.get('email', '').strip()
            if not email:
                errors.append('Email é obrigatório')
            elif '@' not in email or '.' not in email:
                errors.append('Email inválido')
        
        if not is_update or 'instituicao' in data:
            if not data.get('instituicao', '').strip():
                errors.append('Instituição é obrigatória')
        
        if not is_update or 'pais' in data:
            if not data.get('pais', '').strip():
                errors.append('País é obrigatório')
        
        return errors
