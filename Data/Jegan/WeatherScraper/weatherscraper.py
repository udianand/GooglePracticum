from bs4 import BeautifulSoup
from datetime import datetime
#from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3
from geopy.distance import vincenty
from geopy.exc import GeopyError

import pandas as pd
import requests

API_KEY = 'AIzaSyBtwGof1wYOvwKK226kPQV1VyMMz6uTN14'

START_YEAR = 1986

COUNTIES = ['mclean', 'livingston', 'champaign', 'la-salle']
COUNTY_STATE_DICT = {'mclean':'il', 'livingston':'il', 'champaign':'il', 'la-salle':'il'}

COLUMNS = ['COUNTY', 'YEAR', 'MONTH', 'TMP_HIGH', 'TMP_AVG', 'TMP_LOW', 
           'DP_HIGH', 'DP_AVG', 'DP_LOW', 'HUM_HIGH', 'HUM_AVG', 'HUM_LOW',
           'SEALVL_HIGH', 'SEALVL_AVG', 'SEALVL_LOW', 'VIS_HIGH', 'VIS_AVG',
           'VIS_LOW', 'WIND_HIGH', 'WIND_AVG', 'PRECIP', 'NUMDAY_RAIN',
           'NUM_DAYS_SNOW', 'NUM_DAYS_FOG', 'NUM_DAYS_THNDRSTRM']

MONTHS = ['JAN', 'FEB', 'MAR', 'ARP', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
STATE_ABBREV_DICT = { 'alabama':'al', 'alaska':'ak', 'arizona':'az', 'arkansas':'ar', 'california':'ca', 
                     'colorado':'co', 'connecticut':'CT', 'delaware':'de', 'district of columbia':'dc', 
                     'florida':'fl', 'georgia':'ga', 'hawaii':'hi', 'idaho':'id', 'illinois':'il', 
                     'indiana':'in', 'iowa':'ia', 'kansas':'ks', 'kentucky':'ky', 'louisiana':'la', 
                     'maine':'me', 'montana':'mt', 'nebraska':'ne', 'nevada':'nv', 'new hampshire':'nh', 
                     'new jersey':'nj', 'new mexico':'nm', 'new york':'ny', 'north carolina':'nc', 
                     'north dakota':'nd', 'ohio':'oh', 'oklahoma':'ok', 'oregon':'or', 'maryland':'md', 
                     'massachusetts':'ma', 'michigan':'mi', 'minnesota':'mn', 'mississippi':'ms', 
                     'missouri':'mo', 'pennsylvania':'pa', 'rhode island':'ri', 'south carolina':'sc', 
                     'south dakota':'sd', 'tennessee':'tn', 'texas':'tx', 'utah':'ut', 'vermont':'vt', 
                     'virginia':'va', 'washington':'wa', 'west virginia':'wv', 'wisconsin':'wi', 'wyoming':'wy'}

URL_COUNTY_INFO = 'https://en.wikipedia.org/wiki/List_of_counties_by_U.S._state'
URL_WEATHER_HISTORY_TEMPLATE = "https://www.wunderground.com/history/airport/%s/%s/1/1/CustomHistory.html?dayend=31&monthend=12&yearend=%s&req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo="

def get_airport_data():
    print 'GENERATING AIRPORT DATA'
    url = 'https://en.wikipedia.org/wiki/List_of_airports_in_the_United_States'
    result = requests.get(url)
    soup = BeautifulSoup(result.content, 'html.parser')
    table = soup.find_all('table')[2].find_all('td')
    table_end = False
    airport_list = []
    for i, row in enumerate(table):
        if 'wiki' in str(row).lower() and 'airport' not in str(row).lower() and not table_end:
            if 'samoa' in str(row).lower():
                table_end = True
                break
            airport_code = str(table[i+3].text)
            if len(airport_code) == 4:
                geolocator = GoogleV3(api_key=API_KEY)
                geoloc = geolocator.geocode(airport_code, timeout=10)
                if geoloc:
                    row = [airport_code, geoloc.latitude, geoloc.longitude]
                    print row
                    airport_list.append(row)
    return airport_list

def get_closest_airport_id(airport_data, loc):
    index = 0
    min_dist = 100000000000000
    for i, row in enumerate(airport_data):
        if vincenty(loc, (row[1],row[2])).miles < min_dist:
            min_dist = vincenty(loc, (row[1],row[2])).miles
            index = i
    return airport_data[index][0]

def get_county_data():
    airport_data = get_airport_data()
    print 'GENERATING COUNTY DATA'
    result = requests.get(URL_COUNTY_INFO)
    soup = BeautifulSoup(result.content, 'html.parser')
    county_list = []
    for row in soup.find_all('a'):
        if ',' in str(row).lower():
            try:
                county_list.append(str(row.contents[0]))
            except UnicodeEncodeError: # Take care of one stupid county
                if 'new mexico' in str(row).lower():
                    county_list.append('Dona Ana County, New Mexico')
    
    # get rid of garbage data in the beginning of list
    if 'wikipedia' in county_list[0]:
        county_list = county_list[1:]
    last_index = 0

    # get rid of garbage data at the end of the list
    for i in range(len(county_list)):
        if 'wikipedia' in str(county_list[i]):
            last_index = i - 1
            break

    county_list = county_list[:last_index]     
    geolocator = GoogleV3(api_key=API_KEY, timeout=10)
    
    # create county to airport code mapping table
    c_data = []
    
    for i in range(len(county_list)):
        try:
            county = county_list[i].split(',')[0].strip().lower().replace(' county', '')
            state = county_list[i].split(',')[1].strip().lower()
            abbrev = STATE_ABBREV_DICT[state]
            
            # Give three tries, skip if fails every time
            geoloc = None
            try:
                geoloc = geolocator.geocode(county_list[i])
            except GeopyError:
                try:
                    geoloc = geolocator.geocode(county_list[i])
                except GeopyError:
                    try: 
                        geoloc = geolocator.geocode(county_list[i])
                    except GeopyError:
                        print 'Skipping %s' % (county_list[i])
                    
            if geoloc:
                location = (geoloc.latitude, geoloc.longitude)
                airport_code = get_closest_airport_id(airport_data,location)
                c_data.append([county, abbrev, airport_code])
            print county_list[i]
        except IndexError:
            print county_list[i] + ' index error'
        except ValueError:
            print county_list[i] + ' value error'
        except KeyError:
            print county_list[i] + ' value error'
        
    df = pd.DataFrame(c_data,columns=['COUNTY', 'ABBREVIATION', 'AIRPORT CODE'])
    df.to_csv('geo_data.csv')
    
def get_county_list():
    county_list = []
    f = open('county_list.txt','r')
    for line in f:
        county = line.split(',')[0].strip().lower()
        state = line.split(',')[1].strip().lower()
        county_list.append((county, state))
    return county_list

def retreive_geo_data_from_file():
    df = pd.read_csv('geo_data.csv')
    return df
            
def get_weather_data(county, airport, year):
    url = URL_WEATHER_HISTORY_TEMPLATE % (airport, year, year)
    result = requests.get(url)
    soup = BeautifulSoup(result.content, 'html.parser')
    table = soup.find('table', attrs={'id':'obsTable'})
    weather_data = []
    monthly_data = []
    month_index = 0
    for row in (table.find_all('tbody')[1:] + table.find_all('tbody')[:1]):
        daily_row_data = []
        for col in row.find_all('span'):
            try:
                daily_row_data.append(int(col.contents[0]))  
            except ValueError:
                try:
                    daily_row_data.append(float(col.contents[0]))  
                except ValueError:
                    daily_row_data.append(str(col.contents[0]))  
        # single case to avoid one missing day in KBUR
        # extract these case to a method in the future
        if daily_row_data == [] and not (airport == 'KBUR' and month_index == 1 and year == 2008 and len(monthly_data) < 25):
            row_data = [county, year, MONTHS[month_index]]
            try:
                high_temp = max([x[0] for x in monthly_data])
                row_data.append(high_temp)
                avg_temp = sum([x[1] for x in monthly_data])/float(len(monthly_data))
                row_data.append(avg_temp)
                low_temp = min([x[2] for x in monthly_data])
                row_data.append(low_temp)
                high_dp = max([x[3] for x in monthly_data])
                row_data.append(high_dp)
                avg_dp = sum([x[4] for x in monthly_data])/float(len(monthly_data))
                row_data.append(avg_dp)
                low_dp = min([x[5] for x in monthly_data])
                row_data.append(low_dp)
                high_humidity = max([x[6] for x in monthly_data])
                row_data.append(high_humidity)
                avg_humidity = sum([x[7] for x in monthly_data])/float(len(monthly_data))
                row_data.append(avg_humidity)
                low_humidity = min([x[8] for x in monthly_data])
                row_data.append(low_humidity)
                high_sea_lvl = max([x[9] for x in monthly_data])
                row_data.append(high_sea_lvl)
                avg_sea_lvl = sum([x[10] for x in monthly_data])/float(len(monthly_data))
                row_data.append(avg_sea_lvl)
                low_sea_lvl = min([x[11] for x in monthly_data])
                row_data.append(low_sea_lvl)
                high_visibility = max([x[12] for x in monthly_data])
                row_data.append(high_visibility)
                avg_visibility = sum([x[13] for x in monthly_data])/float(len(monthly_data))
                row_data.append(avg_visibility)
                low_visibility = min([x[14] for x in monthly_data])
                row_data.append(low_visibility)
                high_wind = max([x[15] for x in monthly_data])
                row_data.append(high_wind)
                avg_wind = sum([x[16] for x in monthly_data])/float(len(monthly_data))
                row_data.append(avg_wind)
                total_precip = sum([x[17] for x in monthly_data])
                row_data.append(total_precip)
                days_rained = len([x for x in monthly_data if 'rain' in x[18].lower()])
                row_data.append(days_rained)
                days_snowed = len([x for x in monthly_data if 'snow' in x[18].lower()])
                row_data.append(days_snowed)
                days_fog = len([x for x in monthly_data if 'fog' in x[18].lower()])
                row_data.append(days_fog)
                days_thundersorm = len([x for x in monthly_data if 'thunderstorm' in x[18].lower()])
                row_data.append(days_thundersorm)
                monthly_data = []
            except ValueError:
                print 'NO DATA FOR MONTH:%s YEAR:%s' % (MONTHS[month_index], year)
            month_index += 1
            weather_data.append(row_data)
        else:
            if len(daily_row_data) >= 18:
                if len(daily_row_data) == 19:
                    del daily_row_data[17]
                if daily_row_data[17] == 'T': # precipitation less than 0.01
                    daily_row_data[17] = 0.005 # replaced with avg value less than 0.01
                daily_row_data.append(str(row.find_all('td')[-1])) 
                monthly_data.append(daily_row_data)
    return weather_data

def print_to_csv(data):
    w_df = pd.DataFrame(data,columns=COLUMNS)
    w_df.to_csv('weather_data.csv')

import os.path
if not os.path.isfile('geo_data.csv'):
    get_county_data() 
    
today = datetime.today()
end_date_year = 2016
year_list = list(range(START_YEAR, end_date_year+1))
  
geo_data = retreive_geo_data_from_file()
geo_data.drop(geo_data.columns[[0]], axis=1, inplace=True)
  
w_data = []
for county in get_county_list():
    county_data = geo_data[(geo_data['COUNTY'] == county[0].replace(' ', '')) & (geo_data['ABBREVIATION'] == county[1])]
    county_data.index = pd.RangeIndex(len(county_data.index))
    county_data.index = range(len(county_data.index))
    print 'GATHERING WEATHER DATA FOR ...'
    print county_data
    for y in year_list:
        airport = county_data.at[0,'AIRPORT CODE']
        try:
            w_data.extend(get_weather_data(county[0],airport,y))
        except AttributeError:
            print 'Year %s predates this airport' % y
    if end_date_year == today.year:
        w_data = w_data[:-1] # remove current month because data isnt complete
    
print_to_csv(w_data)