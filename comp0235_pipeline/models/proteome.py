from sqlalchemy import Column, Integer, Float, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Proteomes(Base):
    __tablename__ = 'proteomes'
    id = Column(String, primary_key=True)
    description = Column(String)
    sequence = Column(String)