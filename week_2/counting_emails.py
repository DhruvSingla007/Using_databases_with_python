# importing sqlite
import sqlite3

import re

# Checking connection to the database and if the database is not present this command will create one 
conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

# Delete the table if the table already exists
cur.execute('''
DROP TABLE IF EXISTS Users
''')

# Creating a new Table named Users
cur.execute('''
CREATE TABLE Users(email TEXT, count INTEGER)
''')

# grabbing the file
fileName = input("Enter the file name : ")
fhandle = open(fileName,'r')

for line in fhandle:
    emailList = re.findall('^From:.*@(\S+)', line)
    if len(emailList) == 0 : continue
    email = emailList[0]
    cur.execute('SELECT count FROM Users WHERE email = ?', (email,))
    row = cur.fetchone()

    if row is None:
        cur.execute('''
        INSERT INTO Users (email, count) VALUES (?,1) 
        ''', (email,))
    else :
        cur.execute('''
        UPDATE Users SET count = count + 1 WHERE email = ?
        ''',(email,))
    
    conn.commit()

sqlstr = 'SELECT email, count FROM Users ORDER BY count DESC LIMIT 10'

for (e, c) in cur.execute(sqlstr):
    print(e, c)

cur.close()

