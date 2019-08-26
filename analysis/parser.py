import os

#create directory to store cleaned files
dir = "cleanedFiles"
rawFileDir = "scrapedFiles"

if not (os.path.exists(dir)):
    os.mkdir(dir)

log = "logCleanedFiles.txt"
#Store action log
fLog = open(log, 'w+')


for page in os.listdir(rawFileDir):
    #removes all of the html tags and stores in cleanedFiles
    f = open(dir + '/' + page, 'w+')
    with open(rawFileDir + '/' + page, 'r') as prev:
        startWriting = False
        stopWriting = False
        for line in prev:
            if "MxM banner" in line:
                stopWriting = True
            if (startWriting):
                if (not stopWriting):
                    #remove html tags
                    line = line.replace("<br>", "")
                    line = line.replace("</div>", "")
                    line = line.replace("&amp;", "")
                    line = line.replace("&quot;", "")
                    f.write(line)
            else:
                if "Usage of azlyrics.com content" in line:
                    startWriting = True
        f.close()
        if (startWriting and stopWriting):
            fLog.write("Write successful for: "  + page + "\n")
        else:
            fLog.write("Write error for: "  + page + "\n")
fLog.close()

#Prints all the files that need to be cleaned by hand
for page in os.listdir(dir):
    with open(dir + '/' + page, 'r') as prev:
        for line in prev:
            if ("<" in line) or (">" in line):
                print("Check ", page)
                break
            if ("[" in line) or ("]" in line):
                print("Check ", page)
                break
