from bronze.weather import WeatherBronze
from bronze.flights import FlightsBronze
from ref.airports import AirportReference
from api.weather import WeatherAPI
from api.flights import FlightsAPI
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
    end_date = current_date + timedelta(days=49)

    err = None
    while current_date <= end_date:
        print(current_date, file=sys.stderr)
        time.sleep(1)
        for airport_id, latitude, longitude in airport_coordinates.values:
            print(airport_id, file=sys.stderr)
            try: 
                airport_day_weather = weather_api.get_day_weather(airport_id, latitude, longitude, current_date)
                airports_weather_dict[airport_id].append((current_date.isoformat(), airport_day_weather))
                airports_weather_dict[airport_id].append((current_date.isoformat(), airport_day_weather))
            except RuntimeError as error:
                err = error
                print(f"Fatal Error: {error}", file=sys.stderr)
                current_date = end_date
                break
        current_date += timedelta(days=1)

    print(json.dumps(airports_weather_dict))
    if err:
        return
    
    weather_bronze.save(airports_weather_dict) 

    return airports_weather_dict

def get_flights(movement):
    flights_api = FlightsAPI()
    flights_bronze = FlightsBronze(movement)

    airports_df = get_airports()
    airport_coordinates = airports_df[["iata", "icao"]]
    airport_flights_dict = {airport : [] for airport in airport_coordinates["iata"].values}

    last_recovered_date = flights_bronze.get_last_recovery_date()
    max_date = '2024-12-31' if last_recovered_date == None else last_recovered_date
    begin_date = datetime.strptime(max_date, "%Y-%m-%d").date() + timedelta(days=1)
    current_date = begin_date
    end_date = current_date + timedelta(days=0)

    err = None
    while current_date <= end_date:
        print(current_date, file=sys.stderr)
        for airport_id, icao in airport_coordinates.values[:1]:
            print(airport_id, file=sys.stderr)
            try: 
                airport_departures = flights_api.airport_flights(icao, current_date, movement[:-1])
                airport_flights_dict[airport_id].append((current_date.isoformat(), airport_departures))
            except RuntimeError as error:
                err = error
                print(f"Fatal Error: {error}", file=sys.stderr)
                current_date = end_date
                break
        current_date += timedelta(days=1)

    print(json.dumps(airport_flights_dict))
    if err:
        return
    
    flights_bronze.save(airport_flights_dict) 

    return airport_flights_dict

if __name__ == "__main__":
    #get_weather()
    get_flights("departures")