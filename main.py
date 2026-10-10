from bronze.weather import WeatherBronze
from ref.airports import AirportReference
from api.weather import WeatherAPI
import pandas as pd
import sys
from datetime import datetime, timedelta, date
#from dateutil.relativedelta import relativedelta

def get_airports():
    airports_ref = AirportReference()

    data = airports_ref.get_airports()
    return pd.DataFrame(data)

def get_weather():
    weather_api = WeatherAPI()
    weather_bronze = WeatherBronze()


    airports_df = get_airports()
    airport_coordinates = airports_df[["iata", "latitude", "longitude"]].values
    airports_weather_dict = {airport : [] for airport in airports_df["iata"].values}

    last_recovered_date = weather_bronze.get_last_recovery_date()
    max_date = '2024-12-31' if last_recovered_date == None else last_recovered_date
    begin_date = datetime.strptime(max_date, "%Y-%m-%d").date() + timedelta(days=1)
    current_date = begin_date
    end_date = current_date + timedelta(days=11)

    while current_date <= end_date:
        for airport_id, latitude, longitude in airport_coordinates:
            try: 
                airport_day_weather = weather_api.get_day_weather(airport_id, latitude, longitude, current_date)
                airports_weather_dict[airport_id].append((current_date, airport_day_weather))
            except RuntimeError as error:
                print(f"Fatal Error: {error}")
                current_date = end_date
                break
        current_date += timedelta(days=1)

    if airports_weather_dict["CDG"][0][1]==None:
        return
    
    weather_bronze.save(airports_weather_dict) 

    return airports_weather_dict

if __name__ == "__main__":
    get_weather()  