# RedsWeather.py
# by Justin Hall - github.com/jwhall - 2015

# Need this to get weather data from Forecast.IO - see https://github.com/ZeevG/python-forecast.io
import forecastio
# Need this for time operations
import datetime
# Need this to read from CSV file that lists schedule
import csv
# Need this to post tweets - see https://github.com/tweepy/tweepy
import tweepy

# Create Twitter class - code ganked from http://videlais.com/2015/03/02/how-to-create-a-basic-twitterbot-in-python/
class TwitterAPI:
    def __init__(self):
        consumer_key = ""  # Fill in your API key info from apps.twitter.com
        consumer_secret = "" # and here
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = "" # and here
        access_token_secret = "" # and here
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def tweet(self, message):
        self.api.update_status(status=message)

forecastio_api_key = "" # This is your forecast.io API key

# This is the array with all MLB ballparks and their lat/long, for forecast.io to use
teams = [
	["cin", 39.096962, -84.503789, "Cincinnati"], 
	["stl", 38.627003, -90.199404, "St. Louis", "Whiny Birds"], 
	["col", 39.755942, -104.993983, "Denver", "Rockies"],
	["nym", 40.755385, -73.846364, "New York", "Mets"],
	["nyy", 40.829643, -73.926175, "New York", "Yankees"],
	["bos", 42.346676, -71.097218, "Boston", "Red Sox"],
	["chw", 41.829890, -87.633485, "Chicago", "White Sox"],
	["chc", 41.948438, -87.655333, "Chicago", "Cubs"],
	["laa", 41.948438, -87.655333, "Anaheim", "Angels"],
	["oak", 37.751595, -122.200546, "Oakland", "Athletics"],
	["sf", 37.751595, -122.200546, "San Francisco", "Giants"],
	["sd", 32.707709, -117.157085, "San Diego", "Padres"],
	["cle", 41.496211, -81.685229, "Cleveland", "Indians"],
	["kc", 39.051105, -94.481087, "Kansas City", "Royals"],
	["tor", 43.641438, -79.389353, "Toronto", "Blue Jays"],
	["ari", 33.445645, -112.066713, "Arizona", "D-backs"],
	["mia", 25.778665, -80.22028, "Miami", "Marlins"],
	["pit", 40.446855, -80.005666, "Pittsburgh", "Pirates"],
	["mia", 43.027978, -87.97115, "Milwaukee", "Brewers"],
	["det", 42.338998, -83.04852, "Detroit", "Tigers"],
	["min", 44.981708, -93.277338, "Minnesota", "Twins"],
	["bal", 39.283918, -76.621757, "Baltimore", "Orioles"],
	["hou", 29.757268, -95.355519, "Houston", "Astros"],
	["tex", 32.751145, -97.082458, "Texas", "Rangers"],
	["was", 38.873010, -77.007433, "Washington", "Nats"],
	["sea", 47.591488, -122.332308, "Seattle", "Mariners"],
	["tb", 27.768225, -82.653392, "Tampa Bay", "Rays"],
	["atl", 33.734808, -84.389973, "Atlanta", "Braves"],
	["lad", 34.072736, -118.240616, "Los Angeles", "Dodgers"],
	["phi", 39.906057, -75.166495, "Philadelphia", "Phillies"]
]

# You will need a CSV file with three columns - date, time, and location of each MLB game. Mine is called 2015.csv and it sits in the same working dir as the script.
with open('2015.csv') as csvfile:
	reader = csv.DictReader(csvfile)  # Read in the CSV file
	for row in reader:
		if row['date'] == datetime.date.today().strftime("%m/%d/%Y"):  # Compare each line to today's date, and if it's there, create our twitter status
			gametime = datetime.datetime.strptime(row['date'] + " " + row['time'], "%m/%d/%Y %I:%M%p")  # Turn the gametime in the CSV into something Forecast.IO can use
			loc = row['location'] # Set our location to the one in the CSV
			for i in teams:
				if i[0] == loc: # find the location in the teams list
					lat = i[1] # grab its lat and long
					lng = i[2]
					forecast = forecastio.load_forecast(api_key, lat, lng, time=gametime) # pull a forecast data block from the API
					gamecast = forecast.currently() # pull the forecast data from that block for the 'current' time (which is our game time)
					if loc == "cin": # write a different status for a home game
						status = "Forecast for today's " + row['time'] + " gametime is " + gamecast.summary.lower() + " and " + str(int(gamecast.temperature)) + "ºF at Great American Ballpark against the " + i[4] + "."
					else: # otherwise write an away game status
						status = "Forecast for today's " + row['time'] + " gametime is " + gamecast.summary.lower() + " and " + str(int(gamecast.temperature)) + "ºF in " + i[3] + " vs the " + i[4] + "."
						
if __name__ == "__main__" and status != "": # If our status is empty, there's no game today, so do not post.
    twitter = TwitterAPI()
    twitter.tweet(status)
