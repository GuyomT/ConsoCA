from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from configparser import ConfigParser

Base = declarative_base()

class EnergyData(Base):
    __tablename__ = 'energy_data'
    id = Column(Integer, primary_key=True)
    heure = Column(DateTime, unique=True)
    charge_au_nb = Column(Float)
    demande_au_nb = Column(Float)
    iso_ne = Column(Integer)
    nmisa = Column(Float)
    quebec = Column(Float)
    nouvelle_ecosse = Column(Float)
    ipe = Column(Float)


config = ConfigParser()
config.read('config.ini')

db_user = config.get('database', 'user')
db_pass = config.get('database', 'password')

engine = create_engine(f'mysql+pymysql://{db_user}:{db_pass}@localhost/consoca')

Base.metadata.create_all(engine)