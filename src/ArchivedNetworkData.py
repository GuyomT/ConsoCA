from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import sys
import os
import time
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from InitDatabase import EnergyData, engine
from sqlalchemy.orm import sessionmaker
from selenium.webdriver.chrome.options import Options
import streamlit as st


class ArchivedNetworkData:

    def __init__(self):
        """
        ArchivedNetworkData constructor
        """
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--log-level=3')
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options)
        self.url: str = "https://tso.nbpower.com/Public/fr/system_information_archive.aspx"
        self.Session = sessionmaker(bind=engine)
        st.code(self.driver.page_source)

    def get_max_year(self):
        """
        Get the max year from the website
        @return: the max year
        """
        try:
            self.driver.get(self.url)
            return int(self.driver.find_element(By.NAME, 'ctl00$cphMainContent$ddlYear').find_elements(By.TAG_NAME, 'option')[0].text)
        except Exception as e:
            print(
                "An error occurred while retrieving the max year from ArchivedNetworkData")
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
            print(
                "An error occurred while retrieving the min year from ArchivedNetworkData")
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
            self.driver.get(
                "https://tso.nbpower.com/Public/fr/system_information_archive.aspx")

            select_element_month = Select(self.driver.find_element(
                By.NAME, 'ctl00$cphMainContent$ddlMonth'))
            select_element_month.select_by_value(str(month))
            select_element_year = Select(self.driver.find_element(
                By.NAME, 'ctl00$cphMainContent$ddlYear'))
            select_element_year.select_by_value(str(year))
            self.driver.find_element(
                By.ID, 'ctl00_cphMainContent_lbGetData').click()

            csv_data = self.driver.find_element(By.TAG_NAME, 'body').text
            if "Erreur" in csv_data:
                print("Archived data not yet available for this month.")
                return pd.DataFrame()

            return pd.read_csv(StringIO(csv_data))

        except Exception as e:
            print("An error occurred while retrieving the data from ArchivedNetworkData")
            print(e)
            return pd.DataFrame()

    def is_data_present_in_database(self, year):
        """
        Check if data for a specific year is already present in the database.
        """
        session = self.Session()
        try:
            result = session.query(EnergyData.heure).filter(
                EnergyData.heure.between(f'{year}-01-01', f'{year}-12-31')).first()
            return result is not None
        except Exception as e:
            print(f"Database query error: {e}")
            return False
        finally:
            session.close()

    def get_all_data(self):
        """
        Get all archived data from the website and store it in a dictionary of DataFrames.
        """
        try:
            min_year = self.get_min_year()
            max_year = self.get_max_year()
            for year in range(min_year, max_year + 1):
                if os.path.exists(f'archive_{year}.csv'):
                    print(
                        f"Data for year {year} already exists in csv. Skipping.")
                    continue
                yearly_data = pd.DataFrame()
                for month in range(1, 13):
                    print(f"Getting data for {month}/{year}")
                    monthly_data = self.get_data_as_df(month, year)
                    if not monthly_data.empty:
                        yearly_data = pd.concat([yearly_data, monthly_data])
                    time.sleep(0.1)
                if not yearly_data.empty:
                    filename = f'archive_{year}.csv'
                    yearly_data.to_csv(filename, index=False)
                    print(f"Aggregated data for year {year}")
                    print(f"Saved data for year {year} in {filename}")

        except Exception as e:
            print("An error occurred while retrieving the data from ArchivedNetworkData")
            print(e)

    def quit_driver(self):
        """
        Quit the driver
        """
        self.driver.quit()

    def insert_data_into_database(self):
        """
        Insert data from CSV files into the MySQL database.
        """
        session = self.Session()
        try:
            for year in range(self.get_min_year(), self.get_max_year() + 1):
                file_name = f'archive_{year}.csv'
                if os.path.exists(file_name):
                    data_df = pd.read_csv(file_name, parse_dates=['HEURE'])
                    data_df.dropna(inplace=True)

                    for _, row in data_df.iterrows():
                        if not session.query(EnergyData).filter_by(heure=row['HEURE']).first():
                            record = EnergyData(
                                heure=row['HEURE'],
                                charge_au_nb=row['CHARGE_AU_NB'],
                                demande_au_nb=row['DEMANDE_AU_NB'],
                                iso_ne=row['ISO_NE'],
                                nmisa=row['NMISA'],
                                quebec=row['QUEBEC'],
                                nouvelle_ecosse=row['NOUVELLE_ECOSSE'],
                                ipe=row['IPE']
                            )
                            session.add(record)
            session.commit()
            print("Data from CSV files inserted into the database successfully.")
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
        finally:
            session.close()
