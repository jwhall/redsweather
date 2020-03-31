##########################################################################################################
##
##  Schedule Modifier for redsweather.py
##
##  Author: Justin Hall
##  github.com/jwhall
##
##  Takes MLB schedule from http://cincinnati.reds.mlb.com/schedule/downloadable.jsp?c_id=cin#csv-format
##  and converts to $year.csv for use with redsweather twitter
##  bot. Took way too long to write, but hey,
##  we're quarantined!
##      - JWH March 31, 2020
##
##  Usage: run the script with a single argument, the input file
##  Will dump $year.CSV (i.e. 2020.csv) to working dir
##
##########################################################################################################

import sys
import csv
import re
import json
import requests
from datetime import datetime

## Create lists for data to reformat

dates = []
times = []
games = []
loc = []

## Check for input file

if len(sys.argv) < 1:
    print("Usage: " + sys.argv[0] + " <input file>")
    exit

infile = sys.argv[1]

## Subs for the names

shortnames = [("Cardinals", "stl"),
("Rockies", "col"),
("Mets", "nym"),
("Yankees", "nyy"),
("Red Sox", "bos"),
("White Sox", "chw"),
("Cubs", "chc"),
("Angels", "laa"),
("Athletics", "oak"),
("Giants", "sf"),
("Padres", "sd"),
("Indians", "cle"),
("Royals", "kc"),
("Blue Jays", "tor"),
("D-backs", "ari"),
("Marlins", "mia"),
("Pirates", "pit"),
("Brewers", "mil"),
("Tigers", "det"),
("Twins", "min"),
("Orioles", "bal"),
("Astros", "hou"),
("Rangers", "tex"),
("Nationals", "was"),
("Mariners", "sea"),
("Rays", "tb"),
("Braves", "atl"),
("Dodgers", "lad"),
("Phillies", "phi"),
("Reds", "cin"),
("St.Louis", "stl"),
("Denver", "col"),
("Flushing", "nym"),
("Bronx", "nyy"),
("Boston", "bos"),
("Chicago", "chw"),
("Chicago", "chc"),
("LosAngeles", "laa"),
("Oakland", "oak"),
("SanFrancisco", "sf"),
("SanDiego", "sd"),
("Cleveland", "cle"),
("KansasCity", "kc"),
("Toronto", "tor"),
("Phoenix", "ari"),
("Miami", "mia"),
("Pittsburgh", "pit"),
("Milwaukee", "mil"),
("Detroit", "det"),
("Minneapolis", "min"),
("Baltimore", "bal"),
("Houston", "hou"),
("Arlington", "tex"),
("Washington", "was"),
("Seattle", "sea"),
("TampaBay", "tb"),
("Atlanta", "atl"),
("LosAngeles", "lad"),
("Philadelphia", "phi"),
("Cincinnati", "cin")]

## Open CSV and read into lists

with open (infile,'r') as sourcefile:   
    reader = csv.DictReader(sourcefile, delimiter=',')
    for row in reader:
        dates.append(row["START DATE"])
        times.append(row["START TIME ET"])
        games.append(row["SUBJECT"])
        loc.append(row["LOCATION"])

## Change dates, swapping full year for short year

for idx, gamedate in enumerate(dates):
    newdate = datetime.__format__(datetime.strptime(gamedate, "%m/%d/%y"), "%m/%d/%Y")
    dates[idx] = newdate

## Remove space between time and PM

for idx, gametime in enumerate(times):
    newtime = gametime.replace(" ", "")
    times[idx] = newtime

## Get rid of non-opponent names, and then swap opponent names for short names

for idx, game in enumerate(games):
    game = game.replace("Reds at ","")
    game = game.replace(" at Reds","")
    for pat,repl in shortnames:
        game = re.sub(pat, repl, game)
    games[idx] = game

## Cut location down to city and swap for short name

for idx, place in enumerate(loc):
    newplace = re.split("-", place)
    newplace = newplace[1].replace(" ","")
    for pat,repl in shortnames:
        newplace = re.sub(pat, repl, newplace)
    loc[idx] = newplace

## Get the current year, use the MLB's API to get Opening Day's date

today = datetime.today()
year = str(today.year)
response = requests.get("http://lookup-service-prod.mlb.com/json/named.org_game_type_date_info.bam?current_sw='Y'&sport_code='mlb'&game_type='R'&season="+year)
dateinfo = response.json()['org_game_type_date_info']
firstgamedate = datetime.fromisoformat(dateinfo["queryResults"]["row"][0]['first_game_date'])

## Dump output file to year.csv, frickin finally

outputfile = year + ".csv"

## Write our CSV

with open(outputfile, mode='w') as output_csv:
    output_write = csv.writer(output_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    output_write.writerow(['date', 'time', 'opponent', 'location'])
    for w,x,y,z in zip(dates, times, games, loc):
        if (datetime.strptime(w, "%m/%d/%Y") >= firstgamedate) and (not re.search("All-Stars", y)): # write everything after opening day, skipping all-star game
            output_write.writerow([w, x, y, z])

exit
