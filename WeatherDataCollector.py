import requests
import json
import itertools

lat = '53.4264'
long  = '-6.2499'
date = '1627776000'
N = 115
count = -1;

for _ in itertools.repeat(None, N):
    
    dateInt = int(date)
    dateInt = dateInt + 86400
    date = str(dateInt)
    
    url = "https://dark-sky.p.rapidapi.com/"+lat+","+long+","+date

    headers = {
         'x-rapidapi-host': "dark-sky.p.rapidapi.com",
         'x-rapidapi-key': "d3821f4992mshb75085364edd07dp1153b9jsndc5501af26f3"
    }

    response = requests.request("GET", url, headers=headers)

    output = json.loads(response.text)
    currently = output['currently']
    print(currently['temperature'])
    wind  = currently['windSpeed']
    temp = currently['temperature']
    windBearing = currently['windBearing']
    rainFall = currently['precipIntensity']
    Cloudcover = currently['cloudCover']
    vis = currently['visibility']
    d = {"Date":date,
        "Data":[{'Temperature':temp, 'Rain': rainFall, 'Wind speed':wind, 'Wind Direction': windBearing, 'Visibility': vis, 'Cloud coverage': Cloudcover}]
        }
    with open('DublinWeather.json', 'a') as fp:
        json.dump(d, fp, indent= 4)
#print(output[:1])
