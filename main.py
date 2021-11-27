import json
from datetime import datetime

def encodeAircraftType(type: str) -> str:
    aircraftType = ["0", "0", "0", "0", "0", "0", "0", "0", "0"]
    #   {'B788', 'B789', 'A320', 'A20N', 'A319', 'A330', 'A21N', 'B772', 'A333'}
    if type == 'B788':
        aircraftType[0] = "1"
    elif type == 'B789':
        aircraftType[1] = "1"
    elif type == 'A320':
        aircraftType[2] = "1"
    elif type == 'A20N':
        aircraftType[3] = "1"
    elif type == 'A319':
        aircraftType[4] = "1"
    elif type == 'A330':
        aircraftType[5] = "1"
    elif type == 'A21N':
        aircraftType[6] = "1"
    elif type == 'B772':
        aircraftType[7] = "1"
    elif type == 'A333':
        aircraftType[8] = "1"

    return " ".join(aircraftType)

def weatherOnDate(date: datetime, dublin: list[object], london: list[object]) -> str:
    dublin_weather = {}
    london_weather = {}
    for day in dublin:
        if day["date"] == date:
            dublin_weather = day
    for day in london:
        if day["date"] == date:
            london_weather = day

    if dublin_weather == {} or london_weather == {}:
        print(date)
    
    return " ".join([
        str(dublin_weather["temp"]), 
        str(dublin_weather["rain"]), 
        str(dublin_weather["wind_speed"]), 
        str(dublin_weather["wind_direction"]),
        str(london_weather["temp"]), 
        str(london_weather["rain"]), 
        str(london_weather["wind_speed"]), 
        str(london_weather["wind_direction"])
    ])



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
    planes = []

    for file in files:
        flight_data.append(json.load(open(file)))
        
    for i in range(len(files)):
        flight = flight_data[i]
        for j in range(len(flight["listOfDates"])):
            date = flight["listOfDates"][j].split("/")
            planes.append(flight["listOfAircrafts"][j])
            cleaned_flight_data.append({
                "date": datetime(int(date[2]), int(date[1]), int(date[0])).date(),
                "plane": flight["listOfAircrafts"][j],
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

    #   print(set(planes))

    with open('flight_weather_data.csv', 'w') as f:
        f.write("# DTemp DRain DWindSpeed DWindDirection LTemp LRain LWindSpeed LWindDirection B788 B789 A320 A20N A319 A330 A21N B772 A333 delta")
        for flight in cleaned_flight_data:
            f.write(weatherOnDate(flight["date"], cleaned_dublin_weather, cleaned_london_weather) + " " + encodeAircraftType(flight["plane"]) + " " + str(flight["delta"]) + "\n")



if __name__ == "__main__":
    main()