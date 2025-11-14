"""
Rota /time para sincronização de relógio
"""
from flask import jsonify, url_for
from datetime import datetime
from app.routes import time_bp
import logging

logger = logging.getLogger(__name__)

@time_bp.route('/time', methods=['GET'])
def get_time():
    """
    GET /api/v1/time
    Retorna o timestamp oficial do servidor para sincronização
    """
    logger.info("Endpoint /time acessado")
    
    agora = datetime.utcnow()
    
    response = {
        'timestamp_utc': agora.isoformat() + 'Z',
        'timezone': 'UTC',
        'epoch_ms': int(agora.timestamp() * 1000),
        '_links': {
            'self': {'href': url_for('time.get_time', _external=True)},
            'agendamentos': {'href': url_for('agendamentos.list_agendamentos', _external=True)},
            'cientistas': {'href': url_for('cientistas.list_cientistas', _external=True)}
        }
    }
    
    logger.info(f"Timestamp retornado: {response['timestamp_utc']}")
    
    return jsonify(response), 200
