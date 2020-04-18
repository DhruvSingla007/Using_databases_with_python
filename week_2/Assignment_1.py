import sqlite3

conn = sqlite3.connect('ages.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Ages')
cur.execute('CREATE TABLE Ages (name VARCHAR(128), age INTEGER)')

cur.execute('DELETE FROM Ages')

cur.execute('''INSERT INTO Ages (name, age) VALUES ('Rhiannin', 40)''')
cur.execute("INSERT INTO Ages (name, age) VALUES ('Travis', 28)")
cur.execute("INSERT INTO Ages (name, age) VALUES ('Jasmyn', 31)")
cur.execute("INSERT INTO Ages (name, age) VALUES ('Jeannie', 28)")
conn.commit()

cur.execute('SELECT hex(name || age) AS X FROM Ages ORDER BY X')
conn.commit()

