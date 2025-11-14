"""
Configurações da aplicação Flask
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuração base"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///instance/telescopio.db')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    COORDENADOR_URL = os.getenv('COORDENADOR_URL', 'http://localhost:3000')
    NOME_TELESCOPIO = os.getenv('NOME_TELESCOPIO', 'Hubble-Acad')
    
    # Regras de negócio
    DURACAO_MINIMA_MINUTOS = 5
    DURACAO_MAXIMA_MINUTOS = 120
    ANTECEDENCIA_MINIMA_HORAS = 24
    MAX_AGENDAMENTOS_ATIVOS_POR_CIENTISTA = 3
    
    # Nome do telescópio para geração de recursos
    NOME_TELESCOPIO = 'Hubble-Acad'

class DevelopmentConfig(Config):
    """Configuração de desenvolvimento"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configuração de produção"""
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
