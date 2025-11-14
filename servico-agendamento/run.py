"""
Ponto de entrada da aplicação Flask
"""
from app import create_app, db
from app.utils.logger import setup_audit_logger
from app.utils.middleware import setup_request_middleware
import os

# Criar aplicação
app = create_app(os.getenv('FLASK_ENV', 'development'))

# Configurar logger de auditoria
setup_audit_logger()

# Configurar middleware
setup_request_middleware(app)

# Adicionar filtro de correlation_id aos loggers
from app.utils.logger import CorrelationIdFilter
for handler in app.logger.handlers:
    handler.addFilter(CorrelationIdFilter())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
