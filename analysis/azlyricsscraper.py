# This script scrapes the links of Taylor Swift lyrics on azlyrics.com
# Adapted from https://www.py4e.com/code3/urllink2.py
# Very fragile, uses regex to parse info

from urllib.request import urlopen
import sqlite3
import ssl
import re
import os
import time

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#Step 1
#store the index to not overload the website
url = 'https://www.azlyrics.com/t/taylorswift.html'
indexPage = "indexTaylorSwift.html"
pageContent = urlopen(url).read()
with open(indexPage, 'wb') as fid:
    fid.write(pageContent)
fid.close()

conn = sqlite3.connect('content.sqlite')
cur = conn.cursor()

cur.execute('''
        CREATE TABLE IF NOT EXISTS AlbumInfo (
            album_id INTEGER PRIMARY KEY,
            album VARCHAR(128),
            year INTEGER
        );
''')

cur.execute('''
        CREATE TABLE IF NOT EXISTS EditionInfo (
            ed_id INTEGER PRIMARY KEY,
            special_ed VARCHAR(128) UNIQUE
        );
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS SongInfo (
        song_id INTEGER PRIMARY KEY,
        title VARCHAR(128),
        link VARCHAR(256),
        album_id INTEGER,
        ed_id INTEGER,
        excluded INTEGER,
        reason VARCHAR(128)
    );
''')
conn.commit()

#Step 2
#Store number of songs per album for easy storage in next step
html = open(indexPage)
totalSongs = 0
albumList = list()
songList = list()
songNumList = list()
album = None
year = None
#Fragile, requires the format to have links after
#""<div id="" class="album">album type: <b>"Album Name"</b> (year)</div>""
songsInAlbum = 0
#start parsing only after id="listAlbum" is seen
seenID = False
for line in html:
    if 'id="listAlbum"' in line:
        seenID = True
    if seenID == True:
        if 'a href=' in line:
            songsInAlbum += 1
        elif 'class="album"' in line:
            # For albumless songs
            if "other songs:" in line:
                album = None
                year = None
                songNumList.append(songsInAlbum)
                albumList += [["N/A", None]]
                songsInAlbum = 0
            else:
                album = re.findall('.*<b>"(.*)"', line)[0]
                year = re.findall('.*</b>.*\(([0-9]*).</div>', line)[0]
                albumList += [[album, year]]
                #Num of songs of prev album
                songNumList.append(songsInAlbum)
                songsInAlbum = 0
    #Append a placeholder for non album's # of songs
songNumList.append(0)

songNumList = songNumList[1:] #remove the first 0
html.close()

#Step 3
#insert albums and songs into sqlite
for ab in albumList:
    cur.execute('''INSERT OR IGNORE INTO AlbumInfo (album, year) VALUES (?, ?)''', (ab[0], ab[1]) )
conn.commit()

html2 = open(indexPage)
counter = 0
index = 0
for line in html2:
    if "a href=" in line and "taylorswift" in line:
        counter += 1
        if (counter > sum(songNumList[:index + 1]) and (len(songNumList) - 1) > index):
            index += 1
        url = re.findall('.*href="(.*)".*target', line)[0]
        title = re.findall('.*blank">(.*)</a>', line)[0]
        #get the special edition if it exists
        if 'span class="comment"' in line:
            ed = re.findall('.*comment">\[(.*)\]</span>', line)
            #remove 'from' if it exists
            try:
                if 'from' in ed[0]:
                    rem = re.findall('from\s(.*)', ed[0])
                    ed = rem
            except:
                pass
            cur.execute('''INSERT OR IGNORE INTO EditionInfo (special_ed) VALUES (?)''', (ed) )
            crsr = cur.execute('''SELECT ed_id FROM EditionInfo WHERE special_ed=?''', (ed))
            result = crsr.fetchone()
            cur.execute('''INSERT OR IGNORE INTO SongInfo (title, link, album_id, ed_id) VALUES (?, ?, ?, ?)''',
                (title, url, (index + 1), result[0]) )
        else:
            cur.execute('''INSERT OR IGNORE INTO SongInfo (title, link, album_id) VALUES (?, ?, ?)''',
             (title, url, (index + 1)) )
    if counter % 50 == 0 : conn.commit()
html2.close()

#ignore songs not in album and songs from the Christmas album, not written by her
crsr = cur.execute('''SELECT song_id FROM SongInfo WHERE album_id NOT IN (?, ?)''', (2, 9))
conn.commit()

#Step 4
#create directory to store scraped files
dir = "scrapedFiles"
if not (os.path.exists(dir)):
    os.mkdir(dir)

#store raw lyrics files
for tup in crsr.fetchall():
    c = cur.execute('''SELECT title, link FROM SongInfo WHERE song_id=?''', (tup[0],))
    result = c.fetchone()
    url = "https://www.azlyrics.com" + result[1][2:]
    #remove spaces in title, make camelcase name for html page
    title = result[0]
    page = title.replace(" ", "") + ".html"
    pageContent = urlopen(url).read()
    with open(dir + '/' + page, 'wb') as fid:
        fid.write(pageContent)
        fid.close()
    print(url)
    time.sleep(100)

cur.close()
