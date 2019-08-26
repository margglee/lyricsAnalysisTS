#Adapted from https://www.py4e.com/
import sqlite3
#Finds the count of songs containing selected groups of words
punct = "!#$%&()*+,-./:;<=>?@[]^_`'{|}~"

dir = "cleanedFiles"

conn = sqlite3.connect('content.sqlite')
cur = conn.cursor()

chosenWords = ['like/liked', 'love/loved', 'lover/lovers', 'hate/hated',
'heart/hearts', 'girl/girls', 'woman/women', 'boy/boys', 'man/men']

aIdList = [1, 3, 4, 5, 6, 7, 8]
albumList = list()
crsr = cur.execute('''SELECT album FROM AlbumInfo WHERE album_id NOT IN (?, ?)''', (2, 9))
result = crsr.fetchall()
for r in result:
    albumList.append(r[0])
dictList = list()
#opening every song of a particular album and store word count
for i in range(len(aIdList)):
    a = aIdList[i]
    d = dict()
    crsr = cur.execute('''SELECT title FROM SongInfo WHERE album_id=?''', (a,))
    result = crsr.fetchall()
    for r in result:
        f = open(dir + '/' + r[0].replace(" ", "") + ".html", 'r')
        f = f.read().lower()
        f = f.translate(str.maketrans('', '', punct))

        for words in chosenWords:
            for word in words.split('/'):
                if word in f:
                    d[words] = d.get(words, 0) + 1
                    break
    dictList.append(d)
conn.close()

#write info into JS file to be represented as a graph
fhand = open('freqOnce.js','w')
fhand.write("freqOnce = [ ['Album'")
for words in chosenWords:
    fhand.write(",'"+words+"'")
fhand.write("]")
for a in range(len(aIdList)):
    fhand.write(",\n['"+albumList[a]+"'")
    for words in chosenWords:
        if words in dictList[a].keys():
            val = dictList[a].get(words)
        else:
            val = 0
        fhand.write(","+str(val))
    fhand.write("]");

fhand.write("\n];\n")
fhand.close()

print("Output written to freqOnce.js")
print("Open freqOnce.html to visualize the data")
