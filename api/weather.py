import requests
import os
from dotenv import load_dotenv

load_dotenv()

class WeatherAPI:
    def __init__(self):
        self.url_base = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
        self.api_key_1 = os.getenv("VISUAL_CROSSING_KEY")
        self.api_key_2 = os.getenv("VISUAL_CROSSING_KEY_BACKUP")
        self.api_key_3 = os.getenv("VISUAL_CROSSING_KEY_BACKUP_2")
        self.api_key_4 = os.getenv("VISUAL_CROSSING_KEY_BACKUP_3")
        self.api_keys = [self.api_key_1, self.api_key_2, self.api_key_3, self.api_key_4]


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

        for i, key in enumerate(self.api_keys):
            params["key"] = key

            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 429:
                if i < len(self.api_keys) - 1: 
                    print(f"Limit reached for API Key {i+1}, using API Key{i+2}")
                    self.api_keys.remove(self.api_keys[i])
                    continue
                else:
                    raise RuntimeError(f"Limit reached for all  keys. See you tomorrow!")
            
            response.raise_for_status()

            return response.json() 
