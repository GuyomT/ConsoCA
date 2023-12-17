import matplotlib.pyplot as plt
import pandas as pd
from InitDatabase import EnergyData, engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import streamlit as st


class PlotData:
    def __init__(self):
        self.Session = sessionmaker(bind=engine)

    def get_data_from_db(self, start_date, end_date):
        session = self.Session()
        try:
            query = session.query(EnergyData).filter(
                EnergyData.heure.between(start_date, end_date))
            data = pd.read_sql(query.statement, engine)
            return data
        except Exception as e:
            print(f"Database query error: {e}")
            return pd.DataFrame()
        finally:
            session.close()

    def plot_data_from_period(self, start_date, end_date, data_column):
        """
        Plot data from the database.
        @param start_date: datetime object
        @param end_date: datetime object
        @param data_column: string
        """
        data = self.get_data_from_db(start_date, end_date)
        if not data.empty:
            plt.figure(figsize=(10, 6))
            plt.plot(data['heure'], data[data_column],
                     label=f'{data_column} from {start_date} to {end_date}')
            plt.title(
                f'Comparaison de {data_column} entre {start_date} et {end_date}')
            plt.xlabel('Temps')
            plt.ylabel(data_column)
            plt.legend()
            plt.show()
            st.pyplot(plt)
        else:
            print("Aucune donnée à afficher.")

    def plot_bar_chart_from_period(self, start_date, end_date, data_column):
        """
        Plot a bar chart from the database.
        @param start_date: datetime object
        @param end_date: datetime object
        @param data_column: string
        """
        data = self.get_data_from_db(start_date, end_date)
        if not data.empty:
            plt.figure(figsize=(10, 6))
            plt.bar(data['heure'], data[data_column])
            plt.title(f'Bar Chart of {data_column} from {start_date} to {end_date}')
            plt.xlabel('Temps')
            plt.ylabel(data_column)
            plt.show()
            st.pyplot(plt)
        else:
            print("Aucune donnée à afficher.")

    def plot_comparison_between_years(self, year1, year2, data_column):
        """
        Plot a chart comparing data from two different years.
        @param year1: int
        @param year2: int
        @param data_column: string
        """
        data_year1 = self.get_data_from_db(datetime(year1, 1, 1), datetime(year1, 12, 31))
        data_year2 = self.get_data_from_db(datetime(year2, 1, 1), datetime(year2, 12, 31))

        if not data_year1.empty and not data_year2.empty:
            plt.figure(figsize=(10, 6))

            data_year1['Normalized Date'] = data_year1['heure'].apply(lambda x: x.replace(year=2000))
            data_year2['Normalized Date'] = data_year2['heure'].apply(lambda x: x.replace(year=2000))

            plt.plot(data_year1['Normalized Date'], data_year1[data_column], label=f'{year1}')
            plt.plot(data_year2['Normalized Date'], data_year2[data_column], label=f'{year2}')

            plt.title(f'Comparaison de {data_column} entre {year1} et {year2}')
            plt.xlabel('Temps')
            plt.ylabel(data_column)
            plt.legend()
            plt.show()
            st.pyplot(plt)
        else:
            print("Aucune donnée à afficher pour l'une des années.")
