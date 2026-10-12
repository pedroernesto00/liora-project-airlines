import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

class Airport:
    base_url = "https://aerodatabox.p.rapidapi.com"

    iata_to_icao = {
        "CDG": "LFPG",  # Paris Charles-de-Gaulle
        "ORY": "LFPO",  # Paris-Orly
        "NCE": "LFMN",  # Nice Côte d'Azur
        "LYS": "LFLL",  # Lyon-Saint-Exupéry
        "MRS": "LFML",  # Marseille-Provence
        "TLS": "LFBO",  # Toulouse-Blagnac
        "BSL": "LFSB",  # Bâle-Mulhouse
    }


    def __init__(self, iata_code):
        load_dotenv()
        api_key = os.getenv("RAPID_API_KEY")

        self.headers = {
            "x-rapidapi-host" : "aerodatabox.p.rapidapi.com",
            "x-rapidapi-key" : api_key,
            "Content-Type": "application/json"
        }

        self.icao_code = self.iata_to_icao[iata_code]

         
    def get_airport_runways(self,):
        endpoint = f"{self.base_url}/airports/icao/{self.icao_code}/runways"

        response = requests.get(endpoint, headers=self.headers) 
        response.raise_for_status()

        return response.json() 

    def airport_departures_arrivals(self, offset_minutes=-120, duration_minutes=240):
        endpoint = f"{self.base_url}/flights/airports/icao/{self.icao_code}"
        params = {
                    "offsetMinutes":f"{offset_minutes}",
                    "durationMinutes":f"{duration_minutes}",
                    "direction":"Both",
                    "withCancelled":"true",
                    "withCodeshared":"true",
                    "withLocation":"false"
                }

        response = requests.get(endpoint, headers=self.headers, params=params) 
        response.raise_for_status()
        
        return response.json()


if __name__ == "__main__" :
    api = Airport("TLS")
    print(api.headers)

    runways = api.get_airport_runways()

    print(runways)    