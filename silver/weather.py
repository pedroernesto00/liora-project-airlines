from config.supabase import ConnectSupabase
from datetime import datetime, timezone
from time import sleep

class WeatherSilver:
    def __init__(self):
        self.supabase = ConnectSupabase()
    
    def _transform_daily(self, airport, day):
        return {
            "airport" : airport,
            "date" : day.get("datetime"),
            "dew" : day.get("dew"),
            "icon" : day.get("icon"),
            "snow" : day.get("snow"),
            "temp" : day.get("temp"),
            "precip" : day.get("precip"),
            "source" : day.get("source"),
            "tempmin": day.get("tempmin"),
            "uvindex": day.get("uvindex"),
            "winddir": day.get("winddir"),
            "hailrisk": day.get("hailrisk"),
            "humidity": day.get("humidity"),
            "pressure": day.get("pressure"),
            "windgust": day.get("windgust"),
            "feelslike": day.get("feelslike"),
            "snowdepth": day.get("snowdepth"),
            "windspeed": day.get("windspeed"),
            "cloudcover": day.get("cloudcover"),
            "conditions": day.get("conditions"),
            "precipprob": day.get("precipprob"),
            "preciptype": day.get("preciptype"),
            "visibility": day.get("visibility"),
            "description": day.get("description"),
            "precipcover": day.get("precipcover"),
            "solarenergy": day.get("solarenergy"),
            "sunset": datetime.fromtimestamp(day.get("sunsetEpoch"), tz=timezone.utc).time().isoformat(),
            "sunrise": datetime.fromtimestamp(day.get("sunriseEpoch"), tz=timezone.utc).time().isoformat(),
            "feelslikemax": day.get("feelslikemax"),
            "feelslikemin": day.get("feelslikemin"),
            "windspeedmax": day.get("windspeedmax"),
            "windspeedmin": day.get("windspeedmin"),
            "windspeedmean": day.get("windspeedmean"),
            "lightningrisk": day.get("lightningrisk"),
            "solarradiation": day.get("solarradiation")
        }

    def _transform_hourly(self, airport, day, hour):
        return {
            "airport" : airport,
            "date" : day,
            "hour" : hour.get("datetime"),
            "dew" : hour.get("dew"),
            "icon" : hour.get("icon"),
            "snow" : hour.get("snow"),
            "temp" : hour.get("temp"),
            "precip" : hour.get("precip"),
            "source" : hour.get("source"),
            "uvindex": hour.get("uvindex"),
            "winddir": hour.get("winddir"),
            "hailrisk": hour.get("hailrisk"),
            "humidity": hour.get("humidity"),
            "pressure": hour.get("pressure"),
            "windgust": hour.get("windgust"),
            "feelslike": hour.get("feelslike"),
            "snowdepth": hour.get("snowdepth"),
            "windspeed": hour.get("windspeed"),
            "cloudcover": hour.get("cloudcover"),
            "conditions": hour.get("conditions"),
            "precipprob": hour.get("precipprob"),
            "preciptype": hour.get("preciptype"),
            "visibility": hour.get("visibility"),
            "solarenergy": hour.get("solarenergy"),
            "lightningrisk": hour.get("lightningrisk"),
            "solarradiation": hour.get("solarradiation")
        }

    def _process(self, records):
        daily_records = []
        hourly_records = []

        for airport_data in records:
            airport = airport_data["airport"]

            for day in airport_data.get("days") or []:
                weather_date = day.get("datetime")

                if not weather_date:
                    continue

                daily_records.append(
                    self._transform_daily(airport, day)
                )

                for hour in day.get("hours") or []:
                    hour_datetime = hour.get("datetime")

                    if not hour_datetime:
                        continue

                    hourly_record = self._transform_hourly(
                        airport,
                        weather_date,
                        hour
                    )

                    hourly_records.append(hourly_record)

        return daily_records, hourly_records

    def save_all_from_bronze(self, date):
        response = (
            self.supabase.client
            .schema("bronze")
            .table("airport_weather")
            .select("airport,date,days")
            .gte("date", date)
            .execute()
        )

        bronze_records = response.data
        
        daily_records, hourly_records = self._process(bronze_records)

        for i in range(0, len(daily_records), 100):
            self.save_daily(daily_records[i:min(i+100, len(daily_records))])
            sleep(1)

        for i in range(0, len(hourly_records), 100):
            self.save_hourly(hourly_records[i:min(i+100, len(hourly_records))])
            sleep(1)

    def save_daily(self, daily_data: list[dict]):
            
        response_daily = self.supabase.insert_ignore_duplicates(
            schema="silver",
            table="weather_daily",
            data=daily_data,
            on_conflict="airport,date"
        )

        return

    def save_hourly(self, hourly_data: list[dict]):
        response_hourly = self.supabase.insert_ignore_duplicates(
            schema="silver",
            table="weather_hourly",
            data=hourly_data,
            on_conflict="airport,date,hour"
        )

        return