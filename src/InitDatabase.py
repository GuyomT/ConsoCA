from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from configparser import ConfigParser
import streamlit as st

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


db_user = st.secrets["connections.mydb"]["username"]
db_pass = st.secrets["connections.mydb"]["password"]

engine = create_engine(f'mysql+pymysql://{db_user}:{db_pass}@localhost/consoca')

# conn = st.connection("mydb", type="sql", autocommit=True)
# df = conn.query("select * from consoca.energy_data")
# st.dataframe(df)
# print(df)
# conn.connect()

Base.metadata.create_all(engine)