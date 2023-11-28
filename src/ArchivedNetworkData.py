from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
class ArchivedNetworkData:

    def __init__(self):
        """
        ArchivedNetworkData constructor
        """
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.url: str = "https://tso.nbpower.com/Public/fr/system_information_archive.aspx"
        self.all_data = {}

    def get_max_year(self):
        """
        Get the max year from the website
        @return: the max year
        """
        try:
            self.driver.get(self.url)
            return int(self.driver.find_element(By.NAME, 'ctl00$cphMainContent$ddlYear').find_elements(By.TAG_NAME, 'option')[0].text)
        except Exception as e:
            print("An error occurred while retrieving the max year from ArchivedNetworkData")
            print(e)
            sys.exit(1)

    def get_min_year(self):
        """
        Get the min year from the website
        @return: the min year
        """
        try:
            self.driver.get(self.url)
            return int(self.driver.find_element(By.NAME, 'ctl00$cphMainContent$ddlYear').find_elements(By.TAG_NAME, 'option')[-1].text)
        except Exception as e:
            print("An error occurred while retrieving the min year from ArchivedNetworkData")
            print(e)
            sys.exit(1)

    def get_data_as_df(self, month, year):
        """
        Get archived data from the website and return it as a DataFrame.
        @param month: the month
        @param year: the year
        @return: DataFrame containing the data
        """
        try:
            self.driver.get("https://tso.nbpower.com/Public/fr/system_information_archive.aspx")

            self.driver.find_element(By.NAME, 'ctl00$cphMainContent$ddlMonth').send_keys(str(month))
            self.driver.find_element(By.NAME, 'ctl00$cphMainContent$ddlYear').send_keys(str(year))
            self.driver.find_element(By.ID, 'ctl00_cphMainContent_lbGetData').click()

            csv_data = self.driver.find_element(By.TAG_NAME, 'body').text

            if "Erreur" in csv_data:
                print("Archived data not yet available for this month.")
                return pd.DataFrame()

            return pd.read_csv(StringIO(csv_data))

        except Exception as e:
            print("An error occurred while retrieving the data from ArchivedNetworkData")
            print(e)
            return pd.DataFrame()

    def get_all_data(self):
        """
        Get all archived data from the website and store it in a dictionary of DataFrames.
        """
        try:
            min_year = self.get_min_year()
            max_year = self.get_max_year()
            ## TODO: Don't look for data that are alraedy in the Database
            for year in range(min_year, max_year + 1):
                yearly_data = pd.DataFrame()
                for month in range(1, 13):
                    print(f"Getting data for {month}/{year}")
                    monthly_data = self.get_data_as_df(month, year)
                    if not monthly_data.empty:
                        yearly_data = pd.concat([yearly_data, monthly_data])

                if not yearly_data.empty:
                    self.all_data[year] = yearly_data
                    print(f"Aggregated data for year {year}")

        except Exception as e:
            print("An error occurred while retrieving the data from ArchivedNetworkData")
            print(e)

    def save_yearly_data_to_csv(self):
        """
        Save the data for each year to a separate CSV file.
        """
        for year, data in self.all_data.items():
            file_name = f'archive_{year}.csv'
            data.to_csv(file_name, index=False)
            print(f"Saved data for year {year} in {file_name}")

    def quit_driver(self):
        """
        Quit the driver
        """
        self.driver.quit()

    def plot_data_from_csv(self, start_year, end_year, month, data_column):
        """
        Plots data from CSV files for a specific month across multiple years.

        @param start_year: The starting year of the data
        @param end_year: The ending year of the data
        @param month: The month for which to plot the data
        @param data_column: The name of the column containing the data to plot
        """
        plt.figure(figsize=(10, 6))
        month_dict = {1: 'JANVIER', 2: 'FÉVRIER', 3: 'MARS', 4: 'AVRIL', 5: 'MAI', 6: 'JUIN', 7: 'JUILLET', 8: 'AOÛT',
                        9: 'SEPTEMBRE', 10: 'OCTOBRE', 11: 'NOVEMBRE', 12: 'DÉCEMBRE'}


archive = ArchivedNetworkData()
archive.get_all_data()
archive.save_yearly_data_to_csv()
archive.quit_driver()