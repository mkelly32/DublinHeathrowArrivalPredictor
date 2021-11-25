import json

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
    for file in files:
        flight_data.append(json.load(open(file)))
        
    for i in range(len(files)):
        flight = flight_data[i]
        for j in flight.keys():
            print(j)

if __name__ == "__main__":
    main()