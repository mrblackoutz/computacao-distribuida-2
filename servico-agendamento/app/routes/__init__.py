"""
Blueprint para rotas da API
"""
from flask import Blueprint
import os

time_bp = Blueprint('time', __name__)
cientistas_bp = Blueprint('cientistas', __name__)
agendamentos_bp = Blueprint('agendamentos', __name__)

# Importar rotas fixas
from app.routes import time_routes, cientista_routes

# Importar rota de agendamento baseado na variável de ambiente USE_LOCK
USE_LOCK = os.getenv('USE_LOCK', 'true').lower() in ('true', '1', 'yes', 'on')

if USE_LOCK:
    print("✅ Sistema usando VERSÃO COM LOCK (Entrega 3 - Produção)")
    from app.routes import agendamento_routes
else:
    print("⚠️ Sistema usando VERSÃO SEM LOCK (Entrega 2 - Demonstração do problema)")
    from app.routes import agendamento_routes_sem_lock
