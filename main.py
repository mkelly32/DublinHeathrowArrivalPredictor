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
    clean_data = []
    for file in files:
        flight_data.append(json.load(open(file)))
        
    for i in range(len(files)):
        flight = flight_data[i]
        for j in range(len(flight["listOfDates"])):
            clean_data.append({
                "date": datetime.strptime(flight["listOfDates"][j]),
                "delta": calculateDelta(flight["listOfDelays"][j][1])
            })
    clean_data.sort(key = lambda item: item.get("date"))
    print(clean_data)

if __name__ == "__main__":
    main()