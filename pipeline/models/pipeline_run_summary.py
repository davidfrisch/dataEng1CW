from sqlalchemy import Column, Integer, Float, String, create_engine, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

SUCCESS = 'SUCCESS'
RUNNING = 'RUNNING'


class PipelineRunSummary(Base):
    __tablename__ = 'pipeline_run_summary'
    run_id = Column(String, primary_key=True)
    status = Column(Enum(SUCCESS, RUNNING, name="status"), nullable=False)
    duration = Column(Float)
    score_std = Column(Float)
    score_gmean = Column(Float)
    date_started = Column(String, nullable=False)
    date_finished = Column(String)
    author = Column(String, nullable=False)

