from sqlalchemy import Column, Integer, Float, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Proteomes(Base):
    __tablename__ = 'proteomes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    accession = Column(String)
    description = Column(String)
    sequence = Column(String)