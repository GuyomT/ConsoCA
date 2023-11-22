from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import sys

class ArchivesDonnéesRéseau:

    def __init__(self):
        """
        Constructeur de la classe ArchivesDonnéesRéseau
        Classe permettant de récupérer les données du réseau de la page https://tso.nbpower.com/Public/fr/system_information_archive.aspx
        """
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.url: str = "https://tso.nbpower.com/Public/fr/system_information_archive.aspx"

    def get_archived_data(self, month, year, file_name):
        """
        Méthode permettant de récupérer les données du réseau pour un mois et une année donnés
        @param month: le mois
        @param year: l'année
        @param file_name: le nom du fichier dans lequel écrire les données
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
            print(e)
            sys.exit(1)

archive = ArchivesDonnéesRéseau()
archive.get_archived_data(8, 2023, 'fichier.csv')
