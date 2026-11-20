# dic = {'CDG': [], 'ORY': [], 'LIL': [], 'NTE': [], 'LIG': [], 'BOD': [], 'TLS': [], 'MPL': [], 'MRS': [], 'NCE': [], 'LYS': []}

# i = 0
# with open("test_arrivals.json", "r") as file:
#     for line in file:
#         if not line.startswith("Cr"):
#            dic[list(dic.keys())[i%11]].append(line)
#            i += 1

# print(dic)


import json
from config.supabase import ConnectSupabase
from datetime import datetime

with open('weather_airports_convertido.json', 'r') as f:
  data = json.load(f)

data = dict(data)
records = []
for airport, weather_data_list in data.items():
            for date, weather_data in weather_data_list:
                if weather_data == None:
                    continue
                record = {
                    "airport": airport,
                    "date": datetime.strptime(date, "%Y-%m-%d").date().isoformat(),
                    "elevation": weather_data.get("elevation"),
                    "days": weather_data.get("days"),
                    "stations": weather_data.get("stations")
                }
                records.append(record)

supabase = ConnectSupabase()
response = supabase.insert(
            schema="bronze",
            table="airport_weather",
            data=records[1000:]
        )