import codecs
import sqlite3
import json

conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()

cur.execute('''SELECT * FROM Locations''')

fhandle = codecs.open('where.js', 'w', "utf-8")
fhandle.write('myData = [\n')

count = 0

for row in cur:
    data = str(row[1])
    try: js = json.loads(data)
    except: continue

    if not('status' in js and js['status'] == 'OK'): continue
    lat = js['results'][0]['geometry']['location']['lat']
    lng = js['results'][0]['geometry']['location']['lng']

    if lat == 0 or lng == 0 : continue
    location = js['results'][0]['formatted_address']
    location = location.replace("'", "")

    try:
        count = count + 1
        if count > 1 : fhandle.write(',\n')
        output = "[" + str(lat) + "," + str(lng) + ", '" + location + "'" + "]"
        fhandle.write(output)
    except:
        continue

fhandle.write("\n];\n")
cur.close()
fhandle.close()