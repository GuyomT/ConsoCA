from EnergyDataHarvest import EnergyDataHarvest
from sqlalchemy.orm import sessionmaker
from InitDatabase import EnergyData, engine
import streamlit as st
from streamlit_autorefresh import st_autorefresh


def getLastRecord():
    """
    Get the last record from the database.
    Use as debug to check if the data is being inserted.
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

    if conn.query("select * from consoca.energy_data").empty:
        energy_data.getArchivedData()
    energy_data.getRealTimeData()
    # energy_data.plotDataFromPeriod('2021-01-01', '2021-01-02', 'quebec')
    # energy_data.plotBarChartFromPeriod('2021-01-01', '2021-01-02', 'quebec')
    # energy_data.plotComparisonBetweenYears('2020', '2021', 'quebec')

    df = conn.query("select * from consoca.energy_data")
    st.dataframe(df)


# if __name__ == '__main__':
#     energy_data = EnergyDataHarvest()
#     if 'data_archived_loaded' not in st.session_state:
#         st.session_state['data_archived_loaded'] = True # set to false after
#         print(st.session_state['data_archived_loaded'])

#     if not st.session_state['data_archived_loaded']:
#         energy_data.getArchivedData()
#         st.session_state['data_archived_loaded'] = True

#     st_autorefresh(interval=300, key="data_refresh")
#     energy_data.getRealTimeData()

#     df = conn.query("select * from consoca.energy_data")
#     st.dataframe(df)
#     last_record = getLastRecord()
#     if last_record is not None:
#         st.write("Dernier enregistrement : ", last_record)
