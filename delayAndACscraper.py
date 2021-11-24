from bs4 import BeautifulSoup
from selenium import webdriver

# Returns an object with flight data {aircraft, [arrivalDelay, departureDelay], date}
def get_flights(flight_id):
    
    # Inlcude the login before grabbing data properly, done by attatching to my own chrome
    # data dir so that the cookies can be used to login automatically
    print('************* GETTING FLIGHTS FOR ID: ' + flight_id + ' *************')
    options = webdriver.ChromeOptions() 
    options.add_argument("user-data-dir=C:/Users/TEST/AppData/Local/Google/Chrome/User Data")
    driver = webdriver.Chrome("C:/Users/TEST/Documents/Selenium/chromedriver", chrome_options=options)
    driver.get('https://uk.flightaware.com/live/flight/' + flight_id + '/history/300');
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    

    arrivals = soup.find('table', attrs = {'class': 'prettyTable fullWidth tablesaw tablesaw-stack'})
    table = arrivals.find('tbody')
    listOfHrefs = []
    listOfDates = []
    listOfAircrafts = []
    listOfDelays = []
    listOfScheduledTakeOffTimes = []
    
    
    for tr in table.findAll('tr'):
        # Try to get the link
        try:
            hrefEl = tr.find('td', attrs = {'class': 'nowrap'})
            hrefEl = hrefEl.find('a')
            listOfHrefs.append(hrefEl['href'])
        except:
            print("Error scanning a row for href")   
        
        # Try to get the date
        try:
            date = tr.findAll('td')[0]
            date = date.find('span')
            date.find('a')
            listOfDates.append(date.getText())
        except:
            print("Error scanning a row for date")   
        
        # Try to get the aircraft type
        try:
            ac = tr.findAll('td')[1]
            ac = ac.find('span')
            ac.find('i')
            listOfAircrafts.append(ac.getText())
        except:
            print("Error scanning a row for ac")   
    
    for href in listOfHrefs:
        res = getDelayAndTakeoffTime(href, driver)
        if(res != "ecnountered error"):
            listOfScheduledTakeOffTimes.append(res.pop())
            listOfDelays.append(res)
        else:
            listOfScheduledTakeOffTimes.append("ecnountered error")
            listOfDelays.append("ecnountered error")
    
    driver.quit()
    """     print("Lengths match up: " + (len(listOfHrefs) == len(listOfAircrafts)
                                & len(listOfHrefs) == len(listOfDelays))) """
    return {
                'listOfDates'                   : listOfDates,
                'listOfAircrafts'               : listOfAircrafts,
                'listOfDelays'                  : listOfDelays,
                'listOfScheduledTakeOffTimes'   : listOfScheduledTakeOffTimes
            }

def getDelayAndTakeoffTime(href, driver):
    driver.get('https://uk.flightaware.com' + href)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    try:
        print("here")
        depDelay = soup.find('div', attrs = {'class':"flightPageDestinationDelayStatus"})
        print("here")
        depDelay = depDelay.find('span')
        print("here")
        arrDelay = soup.find('div', attrs = {'class':"flightPageOriginDelayStatus"})
        print("here")
        arrDelay = arrDelay.find('span')
        print("here")
        takeoffTime = soup.find('div', attrs = {'class':"flightPageDataAncillaryText"})
        takeoffTime = takeoffTime.find('div')
        takeoffTime = takeoffTime.find('span')
        return [depDelay.getText(), arrDelay.getText(), takeoffTime.getText()]
    except:
            print("Error grabbing delay")
            return "ecnountered error"
    
 
#print(getDelay("/live/flight/BAW845/history/20211109/1055Z/EIDW/EGLL"))   
#print(get_flights('BAW837'))
""" flights = ['BAW839', 'BAW831', 'EIN176', 'VIR522', 'EIN152']
for flight_id in flights:
    f = open("Delay features//" + flight_id + "scraped.json", "w")
    f.write(str(get_flights(flight_id)))
    f.close() """







""" ## To test a returned JSON
rec = 
print(len(rec['listOfDates']))
print(len(rec['listOfAircrafts']))
print(len(rec['listOfDelays'])) """

# Find the set of flight IDs to scrape ({...} converts the list to a set)
ids = {"BAW845","EIN158","EIN154","BAW831",
"EIN152","BAW839","EIN176","BAW827",
"BAW837","EIN172","BAW9174","EIN164",
"BAW845","EIN158","EIN154","BAW831",
"EIN152","VIR522","BAW839","BAW827",
"EIN176","EIN168","EIN164","BAW845",
"EIN158","BAW831","EIN152","EIN168",
"EIN154"}
#{'BAW9174'-4, 'BAW837'-80, 'EIN154', 'EIN164', 'EIN172', 'BAW845', 
# 'EIN158', 'EIN168', 'BAW827', 'BAW839', 'BAW831', 'EIN176', 'VIR522', 'EIN152'}