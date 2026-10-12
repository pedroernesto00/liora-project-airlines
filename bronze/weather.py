from config.supabase import ConnectSupabase

class WeatherBronze:
    def __init__(self):
        self.supabase = ConnectSupabase()

    def get_last_recovery_date(self):
        last_date = self.supabase.get_max_value(
                            schema="bronze", 
                            table="airport_weather",
                            column="date")

        return last_date
    
    def save(self, data):
        records = []
        for airport, weather_data_list in data.items():
            for date, weather_data in weather_data_list:
                if weather_data == None:
                    continue
                record = {
                    "airport": airport,
                    "date": date.isoformat(),
                    "elevation": weather_data.get("elevation"),
                    "days": weather_data.get("days"),
                    "stations": weather_data.get("stations")
                }
                records.append(record)
                
        response = self.supabase.insert(
            schema="bronze",
            table="airport_weather",
            data=records
        )

        return response
    