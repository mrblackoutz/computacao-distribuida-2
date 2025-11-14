#!/usr/bin/env python3
"""
Script para criar o schema do banco de dados SQLite
Cria o DB em /tmp (filesystem nativo) e depois copia para o volume
"""

import os
import sys

# Adicionar o diretório do app ao path
sys.path.insert(0, '/app')

def main():
    print("=" * 60)
    print("Inicializando banco de dados SQLite")
    print("=" * 60)
    
    # Importar após adicionar ao path
    from app import db
    from flask import Flask
    
    # IMPORTANTE: Importar modelos para registrar no metadata
    
    # DB sempre em /tmp para evitar problemas de locking em volumes
    db_path = '/tmp/telescopio.db'
    
    print(f"Caminho do DB: {db_path}")
    
    # Remover DB se existir
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"DB anterior removido")
    
    print(f"\nCriando schema em: {db_path}")
    
    # Criar app temporário
    temp_app = Flask(__name__)
    temp_app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    temp_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar DB com o app temporário
    db.init_app(temp_app)
    
    # Criar todas as tabelas
    with temp_app.app_context():
        try:
            # Criar todas as tabelas
            db.create_all()
            print("✓ Tabelas criadas com sucesso!")
            
            # Verificar tabelas criadas
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"✓ Tabelas encontradas: {tables}")
            
            if not tables:
                print("⚠ Nenhuma tabela foi criada!")
                print("Verificando metadata...")
                print(f"Metadata tables: {list(db.metadata.tables.keys())}")
                return 1
            
            # Testar uma query
            result = db.session.execute(db.text('SELECT 1'))
            print("✓ Database está funcional!")
            
            # Informações finais
            db_size = os.path.getsize(db_path)
            print(f"✓ Arquivo criado: {db_path} ({db_size} bytes)")
            
        except Exception as e:
            print(f"✗ Erro ao criar schema: {e}")
            import traceback
            traceback.print_exc()
            return 1
    
    print("\n" + "=" * 60)
    print("Banco de dados inicializado com sucesso!")
    print("=" * 60)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
