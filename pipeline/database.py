import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from pipeline.models.protein_result import ProteinResults
from pipeline.models.proteome import Proteomes
from sqlalchemy.orm import sessionmaker
# psql -U postgres -W -h localhost -c "CREATE DATABASE proteomics;"
# Replace placeholders with your PostgreSQL credentials

def get_engine():
    db_url = "postgresql://postgres:postgres@localhost:5432/proteomics"
    engine = create_engine(db_url)
    return engine
# connect to the database

def create_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

engine = get_engine()
if not database_exists(engine.url):
    print("Creating database {}".format(engine.url))
    create_database(engine.url)

if engine.connect().closed:
    print("Not connected to the database")
else:
    print("Connected to the database")


# create the tables if they don't exist
ProteinResults.__table__.create(engine, checkfirst=True)
Proteomes.__table__.create(engine, checkfirst=True)