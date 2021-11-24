import json

def main():
    f = open('BAW827scraped.json')
    data = json.load(f)
    print(data)

if __name__ == "__main__":
    main()