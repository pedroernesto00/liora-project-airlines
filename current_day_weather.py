import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

# Gets Visual Crossing API Key by accessing secret
def get_api_key():
    load_dotenv()
    return os.getenv("VISUAL_CROSSING_KEY")
    
# Calls API and returns response
def get_day_weather(airport, latitude, longitude):  
    coordinates = f"{latitude},{longitude}" 
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{coordinates}/next7days"
    
    api_key = get_api_key()
    params = {
        "locationNames" : airport,
        "unitGroup" : "metric",
        "elements" : "add:elevation,add:hailrisk,add:latitude,add:lightningrisk,add:longitude,add:resolvedAddress,add:windspeedmax,add:windspeedmean,add:windspeedmin,remove:moonphase,remove:sunrise,remove:sunset",
        "include" : "days,current,alerts,hours",
        "key" : api_key,
        "contentType" : "json"
    }

    response = requests.get(url, params) 
    response.raise_for_status()

    return response.json() 


def exec():
    # Get informations from ref table   
    airports_coordinates = [("CDG", 49.00620, 2.54305)] #[("NCE", 43.66030, 7.20464), ("CDG", 49.00620, 2.54305)]

    airports_weather_dict = {} 

    # Create a dict with new data from API
    for airport in airports_coordinates:
        airport_id, latitude, longitude = airport
        airports_weather_dict[airport_id] = []
        airport_day_weather = get_day_weather(airport_id, latitude, longitude)
        airports_weather_dict[airport_id].append((date.today(), json.dumps(airport_day_weather)))

    print(airports_weather_dict)
    return airports_weather_dict


if __name__ == "__main__":
    exec()