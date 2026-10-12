import requests
import os
import sys
from dotenv import load_dotenv

load_dotenv()

class WeatherAPI:
    def __init__(self):
        self.url_base = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
        api_keys = ["VISUAL_CROSSING_KEY", "VISUAL_CROSSING_KEY_BACKUP",
                         "VISUAL_CROSSING_KEY_BACKUP_2", "VISUAL_CROSSING_KEY_BACKUP_3"]
        self.api_keys = [{"key" : os.getenv(api_key),
                          "is_active" : True } for api_key in api_keys if os.getenv(api_key)]
        
    def get_day_weather(self, airport, latitude, longitude, date):  
        coordinates = f"{latitude},{longitude}" 
        url = f"{self.url_base}/{coordinates}/{date}"
        
        params = {
            "locationNames" : airport,
            "unitGroup" : "metric",
            "elements" : "add:elevation,add:hailrisk,add:latitude,add:lightningrisk,add:longitude,add:resolvedAddress,add:windspeedmax,add:windspeedmean,add:windspeedmin,remove:moonphase,remove:sunrise,remove:sunset",
            "include" : "days,current,alerts,hours",
            "contentType" : "json"
        }

        for i, api_key in enumerate(self.api_keys):
            if not api_key["is_active"]:
                continue

            params["key"] = api_key["key"]

            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 429:
                if i < len(self.api_keys) - 1: 
                    print(f"Limit reached for API Key {i+1}, using API Key{i+2}", file=sys.stderr)
                    self.api_keys[i]["is_active"] = False
                    continue
                else:
                    raise RuntimeError(f"Limit reached for all  keys. See you tomorrow!")
            
            response.raise_for_status()

            return response.json() 
