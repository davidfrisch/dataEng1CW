from sqlalchemy import Column, Integer, Float, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PipelineRunSummary(Base):
    __tablename__ = 'pipeline_run_summary'
    run_id = Column(String, primary_key=True)
    execution_time = Column(Float)
    score_std = Column(Float)
    score_gmean = Column(Float)
    date_created = Column(String)
    author = Column(String)

