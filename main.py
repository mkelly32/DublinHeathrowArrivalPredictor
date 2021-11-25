import json
from datetime import datetime

def calculateDelta(delta: str) -> int:
    if delta == "on time":
        return 0
    else:
        time = delta.split()
        direction = 1 if time[1] == "late" else -1
        return int(time[0]) * direction

def main():
    files = [
        "BAW827scraped.json",
        "BAW831scraped.json",
        "BAW837scraped.json",
        "BAW839scraped.json",
        "BAW845scraped.json",
        "BAW9174scraped.json",
        "EIN152scraped.json",
        "EIN154scraped.json",
        "EIN158scraped.json",
        "EIN164scraped.json",
        "EIN168scraped.json",
        "EIN172scraped.json",
        "EIN176scraped.json"
    ]

    flight_data = []
    cleaned_flight_data = []
    for file in files:
        flight_data.append(json.load(open(file)))
        
    for i in range(len(files)):
        flight = flight_data[i]
        for j in range(len(flight["listOfDates"])):
            date = flight["listOfDates"][j].split("/")
            cleaned_flight_data.append({
                "date": datetime(int(date[2]), int(date[1]), int(date[0])),
                "delta": calculateDelta(flight["listOfDelays"][j][1])
            })
    cleaned_flight_data.sort(key = lambda item: item.get("date"))

    #   cleaned_flight_data is an ordered list of objects. Each object contains a datetime, 
    #   and a delta. A negative delta means the flight arrived early, and a positive
    #   delta means a flight was late. cleaned_flight_data is the cumulative of all the flight data.
    #   print(cleaned_flight_data)

    dublin_weather = json.load(open("DublinAirportWeather.json"))
    cleaned_dublin_weather = []
    for day in dublin_weather["DailyWeather"]:
        cleaned_dublin_weather.append({
            "date": datetime.fromtimestamp(int(day["Date"])).date(),
            "temp": day["Data"][0]["Temperature"],
            "rain": day["Data"][0]["Rain"],
            "wind_speed": day["Data"][0]["Wind speed"],
            "wind_direction": day["Data"][0]["Wind Direction"]
        })

    london_weather = json.load(open("HeathrowWeather.json"))
    cleaned_london_weather = []
    for day in london_weather["DailyWeather"]:
        cleaned_london_weather.append({
            "date": datetime.fromtimestamp(int(day["Date"])).date(),
            "temp": day["Data"][0]["Temperature"],
            "rain": day["Data"][0]["Rain"],
            "wind_speed": day["Data"][0]["Wind speed"],
            "wind_direction": day["Data"][0]["Wind Direction"]
        })

    #   cleaned_dubin_weather and cleaned_london_weather are both lists of objects. (ordered
    #   by date ascending)

if __name__ == "__main__":
    main()