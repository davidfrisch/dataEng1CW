from sqlalchemy import Column, Integer, Float, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProteinResults(Base):
    __tablename__ = 'protein_results'
    run_id = Column(String, primary_key=True)
    query_id = Column(Integer, primary_key=True)
    best_hit = Column(String)
    best_evalue = Column(Float)
    best_score = Column(Float)
    score_mean = Column(Float)
    score_std = Column(Float)
    score_gmean = Column(Float)

