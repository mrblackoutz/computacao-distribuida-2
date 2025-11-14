"""
Seed de dados iniciais - executado automaticamente ao criar as tabelas
"""

from app.models.cientista import Cientista
from app import db
import logging

logger = logging.getLogger(__name__)

def seed_inicial():
    """
    Popula o banco com cientistas iniciais se estiver vazio
    Executado automaticamente ao iniciar a aplicação
    """
    try:
        # Verificar se já existem cientistas
        count = Cientista.query.count()
        
        if count > 0:
            logger.info(f"Banco já possui {count} cientista(s). Pulando seed.")
            return
        
        logger.info("🌱 Populando banco com cientistas iniciais...")
        
        cientistas_iniciais = [
            {
                'nome': 'Marie Curie',
                'email': 'marie.curie@sorbonne.fr',
                'instituicao': 'Universidade de Paris (Sorbonne)',
                'pais': 'França',
                'especialidade': 'Radioastronomia e Física Nuclear'
            },
            {
                'nome': 'Carl Sagan',
                'email': 'carl.sagan@cornell.edu',
                'instituicao': 'Cornell University',
                'pais': 'Estados Unidos',
                'especialidade': 'Astronomia Planetária e Exobiologia'
            },
            {
                'nome': 'Stephen Hawking',
                'email': 'stephen.hawking@cam.ac.uk',
                'instituicao': 'University of Cambridge',
                'pais': 'Reino Unido',
                'especialidade': 'Cosmologia e Buracos Negros'
            },
            {
                'nome': 'Vera Rubin',
                'email': 'vera.rubin@carnegiescience.edu',
                'instituicao': 'Carnegie Institution',
                'pais': 'Estados Unidos',
                'especialidade': 'Matéria Escura e Galáxias'
            },
            {
                'nome': 'Subrahmanyan Chandrasekhar',
                'email': 's.chandrasekhar@uchicago.edu',
                'instituicao': 'University of Chicago',
                'pais': 'Estados Unidos',
                'especialidade': 'Astrofísica Estelar'
            },
            {
                'nome': 'Jocelyn Bell Burnell',
                'email': 'jocelyn.bell@oxford.ac.uk',
                'instituicao': 'University of Oxford',
                'pais': 'Reino Unido',
                'especialidade': 'Pulsares e Radioastronomia'
            },
            {
                'nome': 'Neil deGrasse Tyson',
                'email': 'neil.tyson@hayden.edu',
                'instituicao': 'Hayden Planetarium',
                'pais': 'Estados Unidos',
                'especialidade': 'Astrofísica e Divulgação Científica'
            },
            {
                'nome': 'Cecilia Payne-Gaposchkin',
                'email': 'cecilia.payne@harvard.edu',
                'instituicao': 'Harvard University',
                'pais': 'Estados Unidos',
                'especialidade': 'Composição Estelar'
            },
            {
                'nome': 'Edwin Hubble',
                'email': 'edwin.hubble@caltech.edu',
                'instituicao': 'California Institute of Technology',
                'pais': 'Estados Unidos',
                'especialidade': 'Cosmologia Observacional'
            },
            {
                'nome': 'Galileu Galilei',
                'email': 'galileo.galilei@unipd.it',
                'instituicao': 'Universidade de Pádua',
                'pais': 'Itália',
                'especialidade': 'Astronomia Observacional'
            }
        ]
        
        for dados in cientistas_iniciais:
            cientista = Cientista(
                nome=dados['nome'],
                email=dados['email'],
                instituicao=dados['instituicao'],
                pais=dados['pais'],
                especialidade=dados['especialidade']
            )
            db.session.add(cientista)
            logger.info(f"✅ Cientista criado: {dados['nome']}")
        
        db.session.commit()
        logger.info(f"🎉 {len(cientistas_iniciais)} cientistas criados com sucesso!")
        
    except Exception as e:
        logger.error(f"❌ Erro ao popular banco: {str(e)}")
        db.session.rollback()
