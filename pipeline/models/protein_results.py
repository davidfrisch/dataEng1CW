from sqlalchemy import Float, Column, Enum, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
SUCCESS="SUCCESS"
RUNNING="RUNNING"
PENDING="PENDING"

class ProteinResults(Base):
    __tablename__ = 'protein_results'
    run_id = Column(String, primary_key=True)
    query_id = Column(String, primary_key=True)
    status = Column(Enum(SUCCESS, RUNNING, PENDING, name="status"), nullable=False, default=PENDING)
    best_hit = Column(String)
    best_evalue = Column(Float)
    best_score = Column(Float)
    score_mean = Column(Float)
    score_std = Column(Float)
    score_gmean = Column(Float)

