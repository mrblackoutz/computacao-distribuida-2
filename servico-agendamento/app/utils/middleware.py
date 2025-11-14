"""
Middleware para requisições HTTP
"""
from flask import g, request
from app.utils.logger import get_correlation_id
import logging

def setup_request_middleware(app):
    """Configura middleware para requisições"""
    
    @app.before_request
    def before_request():
        """Executado antes de cada requisição"""
        # Gerar correlation_id
        correlation_id = get_correlation_id()
        g.correlation_id = correlation_id
        
        # Log de entrada
        app.logger.info(
            f"Requisição {request.method} {request.path} recebida",
            extra={'correlation_id': correlation_id}
        )
    
    @app.after_request
    def after_request(response):
        """Executado após cada requisição"""
        correlation_id = g.get('correlation_id', 'no-correlation-id')
        
        # Log de saída
        app.logger.info(
            f"Resposta {response.status_code} para {request.method} {request.path}",
            extra={'correlation_id': correlation_id}
        )
        
        # Adicionar correlation_id no header da resposta
        response.headers['X-Correlation-ID'] = correlation_id
        
        return response
