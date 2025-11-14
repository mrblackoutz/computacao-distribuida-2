"""
Sistema de logging com correlation_id e suporte a auditoria
"""
import logging
import json
from datetime import datetime
from flask import g, has_request_context
import uuid

class CorrelationIdFilter(logging.Filter):
    """Filtro para adicionar correlation_id aos logs"""
    def filter(self, record):
        if has_request_context():
            record.correlation_id = g.get('correlation_id', 'no-correlation-id')
        else:
            record.correlation_id = 'no-correlation-id'
        return True

def get_correlation_id():
    """Obtém ou cria um correlation_id para a requisição atual"""
    if has_request_context():
        if 'correlation_id' not in g:
            g.correlation_id = str(uuid.uuid4())
        return g.correlation_id
    return str(uuid.uuid4())

def log_audit(event_type, details, service='servico-agendamento'):
    """
    Registra um evento de auditoria em formato JSON
    
    Args:
        event_type: Tipo do evento (ex: AGENDAMENTO_CRIADO)
        details: Dicionário com detalhes do evento
        service: Nome do serviço
    """
    audit_log = {
        'timestamp_utc': datetime.utcnow().isoformat() + 'Z',
        'level': 'AUDIT',
        'event_type': event_type,
        'service': service,
        'correlation_id': get_correlation_id(),
        'details': details
    }
    
    # Usar logging.warning para garantir que será registrado
    # (AUDIT não é um nível padrão do Python)
    logger = logging.getLogger('audit')
    logger.warning(json.dumps(audit_log, ensure_ascii=False))

def setup_audit_logger():
    """Configura o logger de auditoria"""
    import os
    
    # Criar diretório de logs se não existir
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    audit_logger = logging.getLogger('audit')
    audit_logger.setLevel(logging.WARNING)
    
    # Handler específico para auditoria
    handler = logging.FileHandler('logs/audit.log')
    handler.setLevel(logging.WARNING)
    
    # Formato simples para auditoria (já é JSON)
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    
    audit_logger.addHandler(handler)
    audit_logger.propagate = False  # Não propagar para o root logger
