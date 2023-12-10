from ArchivedNetworkData import ArchivedNetworkData
from RealTimeNetworkData import RealTimeNetworkData
from PlotData import PlotData

class EnergyDataHarvest:
    def __init__(self):
        self.archived = ArchivedNetworkData()
        self.realTime = RealTimeNetworkData()
        self.plotter = PlotData()

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

    def plotDataFromPeriod(self, start_date, end_date, data_column):
        """
        Plot data from the database from a given period.
        """
        self.plotter.plot_data_from_period(start_date, end_date, data_column)

    def plotBarChartFromPeriod(self, start_date, end_date, data_column):
        """
        Plot data from the database from a given period in a bar chart.
        """
        self.plotter.plot_bar_chart_from_period(start_date, end_date, data_column)

    def plotComparisonBetweenYears(self, year1, year2, data_column):
        """
        Plot data from the database from a given period in a bar chart.
        """
        self.plotter.plot_comparison_between_years(year1, year2, data_column)
