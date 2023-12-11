from EnergyDataHarvest import EnergyDataHarvest
from sqlalchemy.orm import sessionmaker
from InitDatabase import EnergyData, engine
import streamlit as st


def getLastRecord():
    """
    Get the last record from the database.
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        record = session.query(EnergyData).order_by(
            EnergyData.id.desc()).first()
        return record
    except Exception as e:
        print(f"Database query error: {e}")
        return None
    finally:
        session.close()

if __name__ == '__main__':
    energy_data = EnergyDataHarvest()
    conn = st.connection("mydb", type="sql", autocommit=True)
    print(conn.session)
    df = conn.query("select * from consoca.energy_data")
    st.dataframe(df)
    print(df)
    energy_data.getArchivedData()
    # energy_data.getRealTimeData()
    # energy_data.plotDataFromPeriod('2021-01-01', '2021-01-02', 'quebec')
    # energy_data.plotBarChartFromPeriod('2021-01-01', '2021-01-02', 'quebec')
    # energy_data.plotComparisonBetweenYears('2020', '2021', 'quebec')
    # getLastRecord()
