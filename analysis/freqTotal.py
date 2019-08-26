#Adapted from https://www.py4e.com/
import sqlite3
#Finds the total count of words per album, without selected stop words
stopWords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you",
 "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself",
 "she", "her", "hers", "herself", "it", "its", "itself", "they", "them",
 "their", "theirs", "themselves", "what", "which", "who", "whom", "this",
 "that", "these", "those", "am", "is", "are", "was", "were", "be", "been",
 "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a",
 "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
 "of", "at", "by", "for", "with", "about", "against", "between", "into",
 "through", "during", "before", "after", "above", "below", "to", "from", "up",
 "down", "in", "out", "on", "off", "over", "under", "again", "further", "then",
 "once", "here", "there", "when", "where", "why", "how", "all", "any", "both",
 "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not",
 "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will",
 "just", "don", "should", "now", "im", "youre", "youll", "youd", "whos",
 "ill", "dont", "hes", "oh", "ah", "said", "think", "wanna", "its", "cause",
 "ive", "would", "got", "let", "shouldve", "still", "could", "la", "cant", 'ooh',
 'yeah', 'ohoh', 'baby', 'say', 'isnt', 'uh', 'ha', 'id', 'yet', 'well', 'hey',
 'didnt', 'aint', 'youve', 'theres', 'shes', 'wont', 'whoa']

punct = "!#$%&()*+,-./:;<=>?@[]^_`'{|}~"

dir = "cleanedFiles"

conn = sqlite3.connect('content.sqlite')
cur = conn.cursor()

aIdList = [1, 3, 4, 5, 6, 7, 8]
albumList = list()
crsr = cur.execute('''SELECT album FROM AlbumInfo WHERE album_id NOT IN (?, ?)''', (2, 9))
result = crsr.fetchall()
for r in result:
    albumList.append(r[0])
dictList = list()
totalDict = dict()
#opening every song of a particular album and store word count
for i in range(len(aIdList)):
    a = aIdList[i]
    print("Album:", albumList[i])
    d = dict()
    crsr = cur.execute('''SELECT title FROM SongInfo WHERE album_id=?''', (a,))
    result = crsr.fetchall()
    for r in result:
        f = open(dir + '/' + r[0].replace(" ", "") + ".html", 'r')
        for line in f:
            line = line.lower()
            line = line.translate(str.maketrans('', '', punct))
            #print(line)

            for word in line.split():
                if word not in stopWords:
                    d[word] = d.get(word, 0) + 1
                    totalDict[word] = totalDict.get(word, 0) + 1


    for k, v in sorted(d.items(), key=lambda word: word[1], reverse=True)[:10]:
        print("%s: %s" % (k, v))
    dictList.append(d)

#conn.commit()
conn.close()

fhand = open('wordCloud.js','w')
fhand.write("wordCloud = [")
first = True
for k, v in sorted(totalDict.items(), key=lambda word: word[1], reverse=True)[:100]:
    if not first : fhand.write( ",\n")
    first = False
    fhand.write("{text: '"+k+"', size: "+str(v/3)+"}")
fhand.write( "\n];\n")
fhand.close()

print("Output written to wordCloud.js")
print("Open wordCloud.html in a browser to see the vizualization")

chosenWords = ['like', 'love', 'lover', 'hate', 'heart', 'woman', 'girl', 'boy', 'man']
fhand = open('freqTotal.js','w')
fhand.write("freqTotal = [ ['Album'")
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

print("Output written to freqTotal.js")
print("Open freqTotal.html to visualize the data")
