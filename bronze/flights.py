from config.supabase import ConnectSupabase

class FlightsBronze:
    def __init__(self, movement="departures"):
        self.supabase = ConnectSupabase()
        if movement not in (["departures", "arrivals"]):
            raise RuntimeError("Accepted values: departures, arrivals")
        self.movement = movement

    def get_last_recovery_date(self):
        last_date = self.supabase.get_max_value(
                            schema="bronze", 
                            table=f"airport_{self.movement}",
                            column="date")

        return last_date
    
    def save(self, data):
        records = []
        for airport, flights_data_list in data.items():
            for date, flights_data in flights_data_list:
                if flights_data == None:
                    continue
                record = {
                    "airport": airport,
                    "date": date,
                    "flights" : flights_data
                }
                records.append(record)
                
        response = self.supabase.insert(
            schema="bronze",
            table=f"airport_{self.movement}",
            data=records
        )

        return response
    