import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect('tracks.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track
''')

cur.executescript('''
CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')

def look(entries, key):
    found = False
    for entry in entries:
        if found : 
            return entry.text
        if entry.tag == 'key' and entry.text == key:
            found = True
    return None


fileName = "Library.xml"
tree = ET.parse(fileName)
entries = tree.findall('dict/dict/dict')

for entry in entries:
    if look(entry, 'Track ID') is None : continue

    trackName = look(entry, 'Name')
    artistName = look(entry, 'Artist')
    albumName = look(entry, 'Album')
    genre = look(entry,'Genre')
    rating = look(entry,'Rating')
    length = look(entry,'Total Time')
    count = look(entry, 'Play Count')

    if trackName is None or artistName is None or albumName is None or genre is None :
        continue

    cur.execute('''
    INSERT OR IGNORE INTO Artist (name) VALUES (?)
    ''', (artistName,))
    
    cur.execute('''
    SELECT id FROM Artist WHERE name = ?
    ''', (artistName,))
    artist_id = cur.fetchone()[0]

    
    
    cur.execute('''
    INSERT OR IGNORE INTO Album (title, artist_id) VALUES (?,?)
    ''', (albumName,artist_id))

    cur.execute('''
    SELECT id FROM Album WHERE title = ?
    ''', (albumName,))
    album_id = cur.fetchone()[0]

    cur.execute('''
    INSERT OR IGNORE INTO Genre (name) VALUES (?)
    ''', (genre,))
    cur.execute('''
    SELECT id FROM Genre WHERE name = ?
    ''', (genre,))
    genre_id = cur.fetchone()[0]

    cur.execute('''
    INSERT OR REPLACE INTO Track (title, album_id, genre_id, len, rating, count)
    VALUES (?,?,?,?,?,?)
    ''', (trackName, album_id, genre_id, length, rating, count))

    conn.commit()