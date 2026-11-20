import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class Airport:
    def __init__(self):
        self.base_url = "https://aerodatabox.p.rapidapi.com"
        self.api_key = os.getenv("RAPID_API_KEY")

        self.headers = {
            "x-rapidapi-host" : "aerodatabox.p.rapidapi.com",
            "x-rapidapi-key" : self.api_key,
            "Content-Type": "application/json"
        }

    def get_airport_runways(self, iata_code: str):
        endpoint = f"{self.base_url}/airports/iata/{iata_code}/runways"

        response = requests.get(endpoint, headers=self.headers) 
        response.raise_for_status()

        return response.json() 

    def airport_departures_arrivals(self, iata_code, date: str):
        from_date = f"{date}T00:00"
        to_date = f"{date}T11:59"
        endpoint = f"{self.base_url}/flights/airports/iata/{iata_code}/{from_date}/{to_date}"
        params = {  
                    "direction":"Both",
                    "withCancelled":"true",
                    "withCodeshared":"true",
                    "withLocation":"false"
                 }

        response = requests.get(endpoint, headers=self.headers, params=params) 
        response.raise_for_status()
        
        return response.json()

if __name__=="__main__":
    airport = Airport()

    print(airport.airport_departures_arrivals("CDG", "2025-10-15"))