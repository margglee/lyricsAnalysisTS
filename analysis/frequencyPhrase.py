#Adapted from https://www.py4e.com/
import sqlite3
#Finds the count of a selected phrase and groups of words
phrase = "kissing in the rain"
#First index will be the primary version of the word
kissWords = ['kiss', 'kissing', 'kissin', 'kisses']
rainWords = ['rain', 'raining', 'rainin', 'rains']
punct = "!#$%&()*+,-./:;<=>?@[]^_`{|}~"

conn = sqlite3.connect('content.sqlite')
cur = conn.cursor()

loc = "cleanedFiles"
aIdList = [1, 3, 4, 5, 6, 7, 8]
albumList = list()
dictList = list()
crsr = cur.execute('''SELECT album FROM AlbumInfo WHERE album_id NOT IN (?, ?)''', (2, 9))
result = crsr.fetchall()
for r in result:
    albumList.append(r[0])

for a in aIdList:
    d = dict()
    crsr = cur.execute('''SELECT title FROM SongInfo WHERE album_id=?''', (a,))
    songResults = crsr.fetchall()
    for s in songResults:
        f = open(loc + '/' + s[0].replace(" ", "") + ".html", 'r')
        f = f.read().lower();
        f = f.translate(str.maketrans('', '', punct))
        if phrase in f:
            print(s[0])
        kissUsed = False
        for k in kissWords:
            if k in f:
                d[kissWords[0]] = d.get(kissWords[0], 0) + 1
                kissUsed = True
        for r in rainWords:
            if r in f:
                d[rainWords[0]] = d.get(rainWords[0], 0) + 1
                d['rain'] = d.get('rain', 0) + 1
                if kissUsed:
                    d['both'] = d.get('both', 0) + 1
    dictList.append(d)

chosenWords = [kissWords[0], rainWords[0], 'both']
fhand = open('kiss.js','w')
fhand.write("kiss = [ ['Album'")
for word in chosenWords:
    fhand.write(",'"+word+"'")
fhand.write("]")
for a in range(len(aIdList)):
    fhand.write(",\n['"+albumList[a]+"'")
    for word in chosenWords:
        if word in dictList[a].keys():
            val = dictList[a].get(word)
        else:
            val = 0
        fhand.write(","+str(val))
    fhand.write("]");

fhand.write("\n];\n")
fhand.close()

print("Output written to kiss.js")
print("Open kiss.html to visualize the data")
