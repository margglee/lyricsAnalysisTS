# lyricsAnalysisTS
Using Python and SQL to analyze Taylor Swift Lyrics (Summer 2019)

Also uses JavaScript, CSS and HTML for the web interface

This project was for the Coursera course "Capstone: Retrieving, Processing, and Visualizing Data with Python" with Dr Charles Severance.

First, I scraped data from the internet and stored information into SQL. (azlyricsscraper.py)

Then, cleaned the data (removed ? and replace &amp; with 'And' from database and html file names) for further processing. Also, used the album version of the song and kept featured artist's lines for analysis. (parser.py)

Lastly, analyzed and represented data in JavaScript format. (freqOnce.py, freqTotal.py, frequencyPhase.py)

Future task: add features to continue process when interrupted
