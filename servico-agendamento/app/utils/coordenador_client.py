"""
Cliente para comunicação com o Serviço Coordenador
"""
import requests
from flask import current_app
import logging
from app.utils.logger import get_correlation_id

logger = logging.getLogger(__name__)

class CoordenadorClient:
    """Cliente para o serviço de coordenação"""
    
    def __init__(self, base_url=None):
        self.base_url = base_url or current_app.config.get('COORDENADOR_URL', 'http://localhost:3000')
        self.timeout = 5  # segundos
    
    def acquire_lock(self, recurso):
        """
        Tenta adquirir um lock para um recurso
        
        Args:
            recurso: Identificador único do recurso
            
        Returns:
            tuple: (sucesso: bool, mensagem: str)
        """
        correlation_id = get_correlation_id()
        
        logger.info(f"Tentando adquirir lock para o recurso: {recurso}")
        
        try:
            response = requests.post(
                f'{self.base_url}/lock',
                json={
                    'recurso': recurso,
                    'correlation_id': correlation_id
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                logger.info(f"Lock adquirido com sucesso para o recurso: {recurso}")
                return True, "Lock adquirido"
            elif response.status_code == 409:
                logger.info(f"Falha ao adquirir lock para o recurso: {recurso} (recurso ocupado)")
                data = response.json()
                return False, data.get('error', 'Recurso já está travado')
            else:
                logger.error(f"Erro inesperado ao tentar adquirir lock: {response.status_code}")
                return False, f"Erro ao adquirir lock: {response.status_code}"
                
        except requests.exceptions.Timeout:
            logger.error(f"Timeout ao tentar adquirir lock para o recurso: {recurso}")
            return False, "Timeout ao comunicar com serviço de coordenação"
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de rede ao tentar adquirir lock: {str(e)}")
            return False, f"Erro de comunicação: {str(e)}"
    
    def release_lock(self, recurso):
        """
        Libera um lock de um recurso
        
        Args:
            recurso: Identificador único do recurso
            
        Returns:
            tuple: (sucesso: bool, mensagem: str)
        """
        correlation_id = get_correlation_id()
        
        logger.info(f"Liberando lock para o recurso: {recurso}")
        
        try:
            response = requests.post(
                f'{self.base_url}/unlock',
                json={
                    'recurso': recurso,
                    'correlation_id': correlation_id
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                logger.info(f"Lock liberado com sucesso para o recurso: {recurso}")
                return True, "Lock liberado"
            elif response.status_code == 404:
                logger.warning(f"Tentativa de liberar lock não existente: {recurso}")
                return False, "Recurso não estava travado"
            else:
                logger.error(f"Erro inesperado ao tentar liberar lock: {response.status_code}")
                return False, f"Erro ao liberar lock: {response.status_code}"
                
        except requests.exceptions.Timeout:
            logger.error(f"Timeout ao tentar liberar lock para o recurso: {recurso}")
            return False, "Timeout ao comunicar com serviço de coordenação"
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de rede ao tentar liberar lock: {str(e)}")
            return False, f"Erro de comunicação: {str(e)}"
    
    def check_health(self):
        """
        Verifica se o serviço coordenador está disponível
        
        Returns:
            bool: True se o serviço está saudável
        """
        try:
            response = requests.get(f'{self.base_url}/health', timeout=2)
            return response.status_code == 200
        except:
            return False

def gerar_nome_recurso_agendamento(horario_inicio, horario_fim):
    """
    Gera um nome único para o recurso de agendamento
    
    Args:
        horario_inicio: datetime
        horario_fim: datetime
        
    Returns:
        str: Nome do recurso (ex: "Hubble-Acad_2025-12-01T03:00:00Z")
    """
    # Usar apenas o início para identificar o slot
    # Formato: "Hubble-Acad_YYYY-MM-DDTHH:MM:SSZ"
    nome_telescopio = current_app.config.get('NOME_TELESCOPIO', 'Hubble-Acad')
    timestamp = horario_inicio.strftime('%Y-%m-%dT%H:%M:%SZ')
    return f"{nome_telescopio}_{timestamp}"
