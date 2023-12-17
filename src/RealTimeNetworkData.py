from sqlalchemy import desc
import requests
from bs4 import BeautifulSoup
from InitDatabase import EnergyData, engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

class RealTimeNetworkData:
    def __init__(self):
        self.url = "https://tso.nbpower.com/Public/fr/SystemInformation_realtime.asp"
        self.data = None
        self.Session = sessionmaker(bind=engine)

    def get_data(self):
        """
        Get real-time data from the website parsing the HTML.
        """
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            rows = soup.find_all('tr')
            titles = [b.get_text().strip() for b in rows[4].find_all('b')]
            values = [td.get_text().strip() for td in rows[5].find_all('td')]

            self.data = dict(zip(titles, values))
        else:
            print("Failed to retrieve the webpage. Status code:",
                  response.status_code)


    def insert_data_into_database(self):
        """
        Insert real-time data into the database.
        """
        session = self.Session()
        now = datetime.now()
        clean_now = datetime(now.year, now.month, now.day,
                            now.hour, now.minute, now.second)

        try:
            last_record = session.query(EnergyData).order_by(
                desc(EnergyData.heure)).first()

            if last_record and (clean_now - last_record.heure) < timedelta(minutes=5):
                print(
                    "Une donnée a déjà été insérée il y a moins de 5 minutes, insertion annulée.")
            else:
                record = EnergyData(
                    heure=clean_now,
                    charge_au_nb=self.data.get("Charge au NB"),
                    demande_au_nb=self.data.get("Demande au NB"),
                    iso_ne=self.data.get("ISO-NE"),
                    nmisa=self.data.get("EMEC"),
                    quebec=self.data.get("QUEBEC"),
                    nouvelle_ecosse=self.data.get("NOVA SCOTIA"),
                    ipe=self.data.get("PEI")
                )
                session.add(record)
                session.commit()
                print("Real-time data inserted into the database successfully at ", clean_now)
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
        finally:
            session.close()
