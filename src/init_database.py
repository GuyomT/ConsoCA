from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

Base = declarative_base()

class EnergyData(Base):
    __tablename__ = 'energy_data'
    id = Column(Integer, primary_key=True)
    heure = Column(DateTime)
    charge_au_nb = Column(Float)
    demande_au_nb = Column(Float)
    iso_ne = Column(Integer)
    nmisa = Column(Float)
    quebec = Column(Float)
    nouvelle_ecosse = Column(Float)
    ipe = Column(Float)

# Replace 'your_username', 'your_password', 'localhost', 'mydatabase' with your MySQL credentials
engine = create_engine('mysql+pymysql://your_username:your_password@localhost/mydatabase')
Base.metadata.create_all(engine)
