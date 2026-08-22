import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

def get_api_key():
    load_dotenv()
    return os.getenv("RAPID_API_KEY")

def get_airport_arrivals_departures(airport_iata):
    api_key = get_api_key()
    headers = {
        "x-rapidapi-host" : "aerodatabox.p.rapidapi.com",
        "x-rapidapi-key" : api_key,
        "Content-Type": "application/json"
    }

    params = {"offsetMinutes":"-60",
              "durationMinutes":"120",
              "direction":"Both",
              "withCancelled":"true",
              "withCodeshared":"true",
              "withLocation":"false"}

    url = f"https://aerodatabox.p.rapidapi.com/flights/airports/iata/{airport_iata}"

    response = requests.get(url, headers=headers) 
    response.raise_for_status()

    return response.json() 

if __name__ == "__main__":
    data = get_airport_arrivals_departures("CDG")
    print(json.dumps(data, indent=2))