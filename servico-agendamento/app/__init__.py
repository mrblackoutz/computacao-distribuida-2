"""
Fábrica de aplicação Flask
"""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import logging
import os
from config import config

db = SQLAlchemy()

def create_app(config_name='default'):
    """Factory pattern para criar a aplicação Flask"""
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    app.config.from_object(config[config_name])
    
    # IMPORTANTE: Verificar se precisa usar /tmp ANTES de init_app
    # Isso evita problemas de locking em volumes Docker no Windows
    check_and_use_tmp_if_needed(app)
    
    # Inicializar extensões
    db.init_app(app)
    CORS(app)
    
    # Configurar logging
    setup_logging(app)
    
    # Registrar blueprints
    from app.routes import time_bp, cientistas_bp, agendamentos_bp
    app.register_blueprint(time_bp, url_prefix='/api/v1')
    app.register_blueprint(cientistas_bp, url_prefix='/api/v1')
    app.register_blueprint(agendamentos_bp, url_prefix='/api/v1')
    
    # Criar tabelas
    with app.app_context():
        initialize_database(app)
    
    # Rotas
    register_routes(app)
    
    return app

def check_and_use_tmp_if_needed(app):
    """Verifica se o volume tem problemas de locking e usa /tmp se necessário"""
    import sqlite3
    import subprocess
    
    print("[DEBUG] check_and_use_tmp_if_needed called")
    
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    print(f"[DEBUG] Current URI: {db_uri}")
    
    # Só aplicar para SQLite file-based
    if not db_uri.startswith('sqlite:///') or db_uri == 'sqlite:///:memory:':
        print("[DEBUG] Not file-based SQLite, skipping")
        return
    
    # Parse do caminho
    original_db_path = db_uri[len('sqlite:///'):]
    if not os.path.isabs(original_db_path):
        original_db_path = os.path.join(os.getcwd(), original_db_path)
    
    print(f"[DEBUG] Original path: {original_db_path}")
    
    # Criar diretório se não existir
    db_dir = os.path.dirname(original_db_path)
    os.makedirs(db_dir, exist_ok=True)
    print(f"[DEBUG] Directory created/ensured: {db_dir}")
    
    # Testar se consegue criar conexão SQLite no volume COM POOLING
    # (simula comportamento do SQLAlchemy)
    can_use_volume = False
    try:
        print("[DEBUG] Testing volume with concurrent connections (SQLAlchemy-like)...")
        
        # Teste 1: Conexão única
        conn = sqlite3.connect(original_db_path, timeout=1)
        conn.execute('CREATE TABLE IF NOT EXISTS _test (id INTEGER)')
        conn.close()
        print("[DEBUG] Single connection: OK")
        
        # Teste 2: Múltiplas conexões simultâneas (simula pool)
        conns = []
        for i in range(3):
            conn = sqlite3.connect(original_db_path, timeout=1)
            conn.execute('BEGIN IMMEDIATE')  # Tenta lock
            conns.append(conn)
        
        # Cleanup
        for conn in conns:
            conn.rollback()
            conn.close()
        
        # Limpar tabela de teste
        conn = sqlite3.connect(original_db_path, timeout=1)
        conn.execute('DROP TABLE IF EXISTS _test')
        conn.close()
        
        can_use_volume = True
        print("[DEBUG] Concurrent connections test: PASSED")
        
    except Exception as e:
        print(f"[DEBUG] Concurrent connections test FAILED: {e}")
        # Cleanup em caso de erro
        try:
            for conn in conns:
                conn.close()
        except:
            pass
    
    if can_use_volume:
        print("[DEBUG] Volume works perfectly, using it")
        return  # Volume funciona, usar normalmente
    
    # Volume tem problemas - usar /tmp
    print("[DEBUG] Volume has issues, switching to /tmp")
    tmp_db_path = '/tmp/telescopio.db'
    
    # Se não existe em /tmp, criar via init_db.py
    if not os.path.exists(tmp_db_path):
        print("[DEBUG] Running init_db.py...")
        result = subprocess.run(
            ['python3', '/app/init_db.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        print(f"[DEBUG] init_db.py exit code: {result.returncode}")
        # Não importa se falhou, vamos tentar usar /tmp de qualquer forma
    
    # Reconfigurar para usar /tmp
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{tmp_db_path}'
    print(f"[DEBUG] Reconfigured to: sqlite:///{tmp_db_path}")

def ensure_db_directory(app):
    """Garante que o diretório do banco existe"""
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    
    if not db_uri or not db_uri.startswith('sqlite'):
        return
    
    try:
        if db_uri == 'sqlite:///:memory:':
            app.logger.info("Using in-memory SQLite database")
            return
            
        # Parse do caminho do SQLite
        if db_uri.startswith('sqlite:////'):
            db_path = '/' + db_uri[len('sqlite:////'):]
        elif db_uri.startswith('sqlite:///'):
            db_path = db_uri[len('sqlite:///'):]
            if not os.path.isabs(db_path):
                db_path = os.path.join(os.getcwd(), db_path)
        else:
            app.logger.warning(f"Unrecognized SQLite URI format: {db_uri}")
            return
        
        # Criar diretório
        db_dir = os.path.dirname(db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
            app.logger.info(f"Database directory ensured: {db_dir}")
            app.logger.info(f"Database path: {db_path}")
            
            # Verificar permissões
            if not os.access(db_dir, os.W_OK):
                app.logger.error(f"No write permission for directory: {db_dir}")
            
            # Teste de conectividade low-level
            try:
                import sqlite3
                conn = sqlite3.connect(db_path, timeout=1)
                conn.close()
                app.logger.info("Low-level sqlite3 connection successful")
            except Exception as e:
                app.logger.error(f"Low-level sqlite3 connection failed: {e}")
                
    except Exception as e:
        app.logger.error(f"Error ensuring database directory: {e}")

def initialize_database(app):
    """Inicializa o banco de dados (schema já deve estar criado ou será criado aqui)"""
    try:
        # Criar todas as tabelas
        db.create_all()
        
        # Verificar funcionalidade
        result = db.session.execute(db.text('SELECT 1')).fetchone()
        
        if result:
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
            db_location = 'tmp' if '/tmp/' in db_uri else 'volume'
            
            app.logger.info(f"✓ Database initialized successfully")
            app.logger.info(f"✓ Location: {db_location}")
            app.logger.info(f"✓ Tables: {tables}")
            
            # Popular banco com dados iniciais (se vazio)
            from app.utils.seed import seed_inicial
            seed_inicial()
            
    except Exception as e:
        app.logger.error(f"✗ Database initialization failed: {e}")
        import traceback
        app.logger.error(traceback.format_exc())

def register_routes(app):
    """Registra rotas adicionais"""
    @app.route('/')
    def index():
        """Interface web principal"""
        return render_template('index.html')
    
    @app.route('/health')
    def health_check():
        """Endpoint de health check para Docker
        
        Funciona tanto com DB no volume quanto em /tmp
        """
        try:
            # Usar SQLAlchemy diretamente 
            from sqlalchemy import text
            result = db.session.execute(text('SELECT 1')).fetchone()
            
            # Verificar tabelas
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
            db_location = 'tmp' if '/tmp/' in db_uri else 'volume'
            
            return {
                'status': 'healthy',
                'database': 'connected',
                'tables': len(tables),
                'location': db_location
            }, 200
                
        except Exception as e:
            app.logger.error(f'Health check failed: {e}')
            return {'status': 'unhealthy', 'error': str(e)}, 503
    
    return app

def setup_logging(app):
    """Configura o sistema de logging"""
    # Criar diretório de logs se não existir
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Formato padrão (com correlation_id)
    log_format = '[%(levelname)s] %(asctime)s %(name)s %(correlation_id)s: %(message)s'

    class SafeFormatter(logging.Formatter):
        def format(self, record):
            if not hasattr(record, 'correlation_id'):
                record.correlation_id = '-'
            return super().format(record)

    # Handler para arquivo
    file_handler = logging.FileHandler('logs/app.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(SafeFormatter(log_format))

    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(SafeFormatter(log_format))

    # Configurar logger da aplicação
    app.logger.handlers.clear()
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)
