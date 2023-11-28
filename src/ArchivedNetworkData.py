from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import sys
import os

class ArchivedNetworkData:

    def __init__(self):
        """
        ArchivedNetworkData constructor
        """
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.url: str = "https://tso.nbpower.com/Public/fr/system_information_archive.aspx"

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

    def get_data(self, month, year, file_name):
        """
        Get archived data from the website
        @param month: the month
        @param year: the year
        @param file_name: the file name
        """
        try:
            self.driver.get("https://tso.nbpower.com/Public/fr/system_information_archive.aspx")

            self.driver.find_element(By.NAME, 'ctl00$cphMainContent$ddlMonth').send_keys(str(month))
            self.driver.find_element(By.NAME, 'ctl00$cphMainContent$ddlYear').send_keys(str(year))
            self.driver.find_element(By.ID, 'ctl00_cphMainContent_lbGetData').click()

            csv_data = self.driver.find_element(By.TAG_NAME, 'body').text

            with open(file_name, 'w') as file:
                file.write(csv_data)

        except Exception as e:
            print("An error occurred while retrieving the data from ArchivedNetworkData")
            print(e)
            sys.exit(1)

    def get_all_data(self):
        """
        Get all archived data from the website
        """
        try:
            min_year = self.get_min_year()
            max_year = self.get_max_year()

            print(f"Getting data from {min_year} to {max_year}")
            for year in range(min_year, max_year + 1):
                for month in range(1, 13):
                    file_name = f'archive_{month}_{year}.csv'

                    if os.path.exists(file_name):
                        print(f"File {file_name} already exists. Skipping.")
                        continue

                    print(f"Getting data for {month}/{year}")
                    self.get_data(month, year, file_name)
        except Exception as e:
            print("An error occurred while retrieving the data from ArchivedNetworkData")
            print(e)
            sys.exit(1)

    def quit_driver(self):
        """
        Quit the driver
        """
        self.driver.quit()


archive = ArchivedNetworkData()
archive.get_all_data()
archive.quit_driver()