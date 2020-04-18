import urllib.request, urllib.parse, urllib.error
import ssl
import sqlite3
import json

api_key = False

if api_key is False:
    api_key = 42
    service_url = "http://py4e-data.dr-chuck.net/geojson?"
else:
    service_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Locations(
    address TEXT,
    geodata TEXT
)
''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

fhandle = open('where.data')

count = 0
for line in fhandle:

    if count > 200 :
        print('Retrieved 200 locations, restart to retrieve more')
        break

    location = line.strip()

    cur.execute('''
    SELECT geodata FROM Locations WHERE address =  ? 
    ''', (location,))

    try:
        entry = cur.fetchone()[0]
        print('Entry already found in database')
        continue
    except :
        pass

    params = dict()
    params['address'] = location
    if api_key is not False:
        params['key'] = api_key
    
    url = service_url + urllib.parse.urlencode(params)

    urlHandle = urllib.request.urlopen(url,context=ctx)
    urlData = urlHandle.read().decode()
    count = count + 1

    try:
        js = json.loads(urlData)
    except :
        print("==========Failed==========")
        continue

    if 'status' not in js or js['status'] != 'OK' or js['status'] == 'ZERO_RESULTS':
        print("==============FAILED TO RETRIEVE=============")
        continue

    cur.execute('''
    INSERT INTO Locations (address, geodata) VALUES (?,?)
    ''', (location, urlData))

    conn.commit()

