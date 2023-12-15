import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from pipeline.constants import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database
from pipeline.models.protein_results import ProteinResults
from pipeline.models.proteome import Proteomes
from pipeline.models.pipeline_run_summary import PipelineRunSummary
from sqlalchemy.orm import sessionmaker
# psql -U postgres -W -h localhost -c "CREATE DATABASE proteomics;"
# Replace placeholders with your PostgreSQL credentials

def get_engine():
    db_url = DATABASE_URL
    engine = create_engine(db_url)
    return engine
# connect to the database

def create_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

engine = get_engine()


if "--reset" in sys.argv:
    print("Dropping database {}".format(engine.url))
    shouldDelete = input("Are you sure? (y/n)")
    if shouldDelete == "y":
        drop_database(engine.url)
    elif shouldDelete == "n":
        print("Not deleting database")
    else:
        print("Invalid input")
        exit(1)

if not database_exists(engine.url):
    print("Creating database {}".format(engine.url))
    create_database(engine.url)

if engine.connect().closed:
    print("Not connected to the database")
else:
    print("Connected to the database")

# create the tables if they don't exist
PipelineRunSummary.__table__.create(engine, checkfirst=True)
ProteinResults.__table__.create(engine, checkfirst=True)
Proteomes.__table__.create(engine, checkfirst=True)
print("Tables created")