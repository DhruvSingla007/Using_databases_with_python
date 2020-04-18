import sqlite3
import re

conn = sqlite3.connect('counts.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')
cur.execute('CREATE TABLE Counts(org TEXT, count INTEGER)')

fileName = input("Enter the file name : ")
fhandle = open(fileName)

for line in fhandle:
    orgList = re.findall('^From:.*@(\S+)',line)
    if len(orgList) == 0 : continue
    org = orgList[0]

    cur.execute('SELECT count FROM Counts WHERE org = ?', (org,))
    row = cur.fetchone()

    if row is None:
        cur.execute('INSERT INTO Counts (org, count) VALUES (?,1)',(org,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',(org,))

    conn.commit()

sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC'

for (e, c) in cur.execute(sqlstr):
    print(e, c)

cur.close()
