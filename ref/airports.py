from config.supabase import ConnectSupabase

class AirportReference:

    def __init__(self):
        self.supabase = ConnectSupabase()

    def get_airports(self):
        return self.supabase.select(
            schema="ref",
            table="airports"
        )