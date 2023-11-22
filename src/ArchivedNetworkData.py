from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import sys

class ArchivedNetworkData:

    def __init__(self):
        """
        ArchivedNetworkData constructor
        """
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.url: str = "https://tso.nbpower.com/Public/fr/system_information_archive.aspx"

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

            self.driver.quit()
        except Exception as e:
            print("An error occurred while retrieving the data from ArchivedNetworkData .")
            print(e)
            sys.exit(1)

archive = ArchivedNetworkData()
archive.get_data(8, 2023, 'fichier.csv')
