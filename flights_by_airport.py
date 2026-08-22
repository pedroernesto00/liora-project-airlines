import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

def get_api_token():
    load_dotenv()
    return os.getenv("OPENSKY_TOKEN")

def arrivals_by_airport(airport_icao):
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = today - timedelta(days=1)

    yesterday_begin = datetime(yesterday.year, yesterday.month, yesterday.day)
    yesterday_end = today - timedelta(seconds=1)

    begin_unix = int(yesterday_begin.timestamp())
    end_unix = int(yesterday_end.timestamp())
    url = f"https://opensky-network.org/api/flights/arrival?airport={airport_icao}&begin={begin_unix}&end={end_unix}"

    token = get_api_token()
    headers = {
        "Authorization" : f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    response.raise_for_status()

    return response.json()

if __name__ == "__main__":
    data = arrivals_by_airport('LFPG')
    print(json.dumps(data, indent=2))