from ArchivedNetworkData import ArchivedNetworkData
from RealTimeNetworkData import RealTimeNetworkData

class EnergyDataHarvest:
    def __init__(self):
        self.archived = ArchivedNetworkData()
        self.realTime = RealTimeNetworkData()

    def getArchivedData(self):
        """
        Get archived data from the website and insert it into the database.
        """
        self.archived.get_all_data()
        self.archived.insert_data_into_database()
        self.archived.quit_driver()

    def getRealTimeData(self):
        """
        Get real time data from the website and insert it into the database.
        """
        self.realTime.get_data()
        self.realTime.insert_data_into_database()