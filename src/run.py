from EnergyDataHarvest import EnergyDataHarvest
from sqlalchemy.orm import sessionmaker
from InitDatabase import EnergyData, engine

if __name__ == '__main__':
    energy_data = EnergyDataHarvest()
    energy_data.getArchivedData()
    energy_data.getRealTimeData()

    session = sessionmaker(bind=engine)()

    # last_record_by_id = session.query(EnergyData).order_by(EnergyData.id.desc()).first()
    # print(last_record_by_id.charge_au_nb)
    # last_record_by_time = session.query(EnergyData).order_by(EnergyData.heure.desc()).first()
    # print(last_record_by_time.charge_au_nb)
    # session.close()