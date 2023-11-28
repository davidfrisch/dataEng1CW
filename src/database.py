from sqlalchemy import create_engine
from models.protein_result import ProteinResults
from models.proteome import Proteomes
# psql -U postgres -W -h localhost -c "CREATE DATABASE proteomics;"
# Replace placeholders with your PostgreSQL credentials
db_url = "postgresql://postgres:postgres@localhost:5432/proteomics"
engine = create_engine(db_url)

# connect to the database
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()
if engine.connect().closed:
    print("Not connected to the database")
else:
    print("Connected to the database")

# create the tables if they don't exist
ProteinResults.__table__.create(engine, checkfirst=True)
Proteomes.__table__.create(engine, checkfirst=True)