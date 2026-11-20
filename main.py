from bronze.weather import WeatherBronze
from silver.weather import WeatherSilver
from ref.airports import AirportReference
from api.weather import WeatherAPI
import pandas as pd
import sys
import json
import time
from datetime import datetime, timedelta, date


def get_airports():
    airports_ref = AirportReference()

    data = airports_ref.get_airports()
    return pd.DataFrame(data)

def get_weather():
    weather_api = WeatherAPI()
    weather_bronze = WeatherBronze()

    airports_df = get_airports()
    airport_coordinates = airports_df[["iata", "latitude", "longitude"]]
    airports_weather_dict = {airport : [] for airport in airport_coordinates["iata"].values}

    last_recovered_date = weather_bronze.get_last_recovery_date()
    max_date = '2024-12-31' if last_recovered_date == None else last_recovered_date
    begin_date = datetime.strptime(max_date, "%Y-%m-%d").date() + timedelta(days=1)
    current_date = begin_date
    end_date = current_date + timedelta(days=14)
    today = date.today() + timedelta(days=-1)

    err = None
    while current_date <= min(end_date, today):
        print(current_date, file=sys.stderr)
        time.sleep(1)
        for airport_id, latitude, longitude in airport_coordinates.values:
            print(airport_id, file=sys.stderr)
            try: 
                airport_day_weather = weather_api.get_day_weather(airport_id, latitude, longitude, current_date)
                airports_weather_dict[airport_id].append((current_date.isoformat(), airport_day_weather))
            except RuntimeError as error:
                err = error
                print(f"Fatal Error: {error}", file=sys.stderr)
                current_date = end_date
                break
        current_date += timedelta(days=1)
    if err:
        return
    
    weather_bronze.save(airports_weather_dict) 

    return begin_date


if __name__ == "__main__":
    begin_date = get_weather()

    weather_silver = WeatherSilver()
    weather_silver.save_all_from_bronze(begin_date)