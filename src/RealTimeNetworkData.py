import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

class RealTimeNetworkData:
    def __init__(self):
        self.url = "https://tso.nbpower.com/Public/fr/SystemInformation_realtime.asp"
        self.data = None

    def get_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            date = soup.find('i').get_text().strip()
            print(date)

            rows = soup.find_all('tr')
            titles = [b.get_text().strip() for b in rows[4].find_all('b')]
            values = [td.get_text().strip() for td in rows[5].find_all('td')]

            self.data = dict(zip(titles, values))
        else:
            print("Failed to retrieve the webpage. Status code:", response.status_code)

    def process_and_display_data(self):
        if self.data:
            df = pd.DataFrame(list(self.data.items()), columns=['Titre', 'Valeur'])
            df['Valeur'] = pd.to_numeric(df['Valeur'], errors='coerce')
            print(df)

            # Créer et afficher le graphique
            plt.figure(figsize=(10, 6))
            plt.bar(self.data.keys(), df['Valeur'], color='blue')
            plt.title('Visualisation des Données')
            plt.xlabel('Catégories')
            plt.ylabel('Valeurs')
            plt.xticks(rotation=45)
            plt.show()
        else:
            print("No data to display.")

# Utilisation de la classe
donnees = RealTimeNetworkData()
donnees.get_data()
donnees.process_and_display_data()
