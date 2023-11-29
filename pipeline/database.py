from sqlalchemy import create_engine
from comp0235_pipeline.models.protein_result import ProteinResults
from comp0235_pipeline.models.proteome import Proteomes
# psql -U postgres -W -h localhost -c "CREATE DATABASE proteomics;"
# Replace placeholders with your PostgreSQL credentials

def get_engine():
    db_url = "postgresql://postgres:postgres@localhost:5432/proteomics"
    engine = create_engine(db_url)
    return engine
# connect to the database
from sqlalchemy.orm import sessionmaker

def create_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

engine = get_engine()
if engine.connect().closed:
    print("Not connected to the database")
else:
    print("Connected to the database")

# create the tables if they don't exist
ProteinResults.__table__.create(engine, checkfirst=True)
Proteomes.__table__.create(engine, checkfirst=True)