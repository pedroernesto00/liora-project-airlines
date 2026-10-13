import os
import requests
from dotenv import load_dotenv
from datetime import datetime, time, timedelta
from config.opensky_token_manager import TokenManager

load_dotenv()

class FlightsAPI:
    def __init__(self):
        self.base_url = "https://opensky-network.org/api"
        self.token_manager = TokenManager()
   
    def airport_flights(self, icao_code, date, movement="departure"):
        if movement not in ["departure", "arrival"]:
            raise RuntimeError("Accepted values: departure, arrival")
        begin_unix = int(datetime.combine(date, time.min).timestamp())
        end_unix = int(datetime.combine(date, time.max).timestamp())
    
        endpoint = f"{self.base_url}/flights/{movement}?airport={icao_code}&begin={begin_unix}&end={end_unix}"
        headers = self.token_manager.headers()
        
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 404:
            return []

        if response.status_code == 429:
            print("Remaining credits:", response.headers.get("X-Rate-Limit-Remaining"))
            raise RuntimeError("Limit reached, see you tomorrow!")

        response.raise_for_status()
        
        return response.json()

if __name__== "__main__":
    flights = FlightsAPI()
    date = datetime.strptime('2026-10-01', "%Y-%m-%d").date()
    flights.airport_departures("LFBL", date)
