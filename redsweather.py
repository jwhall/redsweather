#!/usr/bin/python
# RedsWeather.py
# by Justin Hall - github.com/jwhall - 2015
# some edits by Alex Kuhl - github.com/alexkuhl

import datetime
import csv
import tweepy     # twitter interface - see https://github.com/tweepy/tweepy

from pyowm import OWM	# Free API from https://openweathermap.org/api, code from https://github.com/csparpa/pyowm
from pyowm.utils import config
from pyowm.utils import timestamps

class TwitterAPI:
    """Twitter interface. Code ganked from http://videlais.com/2015/03/02/how-to-create-a-basic-twitterbot-in-python/  """
    def __init__(self):
        # Twitter API keys from apps.twitter.com
        consumer_key = "fill_in_yours"
        consumer_secret = "fill_in_yours"
        access_token = "fill_in_yours"
        access_token_secret = "fill_in_yours"
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def tweet(self, message):
        self.api.update_status(status=message)

owm_api_key = "fill_in_yours"
owm = OWM(owm_api_key)
mgr = owm.weather_manager()

# dictionary of all MLB ballparks, including latitude and longitude
teams = {
	"cin": [39.096962, -84.503789, "Cincinnati", "Reds"], 
	"stl": [38.627003, -90.199404, "St. Louis", "Whiny Birds"], 
	"col": [39.755942, -104.993983, "Denver", "Rockies"],
	"nym": [40.755385, -73.846364, "New York", "Mets"],
	"nyy": [40.829643, -73.926175, "New York", "Yankees"],
	"bos": [42.346676, -71.097218, "Boston", "Red Sox"],
	"chw": [41.829890, -87.633485, "Chicago", "White Sox"],
	"chc": [41.948438, -87.655333, "Chicago", "Cubs"],
	"laa": [41.948438, -87.655333, "Anaheim", "Angels"],
	"oak": [37.751595, -122.200546, "Oakland", "Athletics"],
	"sf":  [37.751595, -122.200546, "San Francisco", "Giants"],
	"sd":  [32.707709, -117.157085, "San Diego", "Padres"],
	"cle": [41.496211, -81.685229, "Cleveland", "Guardians"],
	"kc":  [39.051105, -94.481087, "Kansas City", "Royals"],
	"tor": [43.641438, -79.389353, "Toronto", "Blue Jays"],
	"ari": [33.445645, -112.066713, "Arizona", "Diamondbacks"],
	"mia": [25.778665, -80.22028, "Miami", "Marlins"],
	"pit": [40.446855, -80.005666, "Pittsburgh", "Pirates"],
	"mil": [43.027978, -87.97115, "Milwaukee", "Brewers"],
	"det": [42.338998, -83.04852, "Detroit", "Tigers"],
	"min": [44.981708, -93.277338, "Minnesota", "Twins"],
	"bal": [39.283918, -76.621757, "Baltimore", "Orioles"],
	"hou": [29.757268, -95.355519, "Houston", "Astros"],
	"tex": [32.751145, -97.082458, "Texas", "Rangers"],
	"was": [38.873010, -77.007433, "Washington", "Nationals"],
	"sea": [47.591488, -122.332308, "Seattle", "Mariners"],
	"tb":  [27.768225, -82.653392, "Tampa Bay", "Rays"],
	"atl": [33.734808, -84.389973, "Atlanta", "Braves"],
	"lad": [34.072736, -118.240616, "Los Angeles", "Dodgers"],
	"phi": [39.906057, -75.166495, "Philadelphia", "Phillies"]
}

if __name__ == "__main__":
    # csv file should have four columns: date,time,location,opponent
    # location and opponent are both listed as the city abbreviations seen above in the dictionary keys
	with open('./test.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if row['date'] == datetime.date.today().strftime("%m/%d/%Y"):  # loop until we find today's date (if it exists in the file)
				gametime = datetime.datetime.strptime(row['date'] + " " + row['time'], "%m/%d/%Y %I:%M%p")  # convert date to forecast.io format
				# search dictionary for the location
				loc = teams[row['location']]
				if loc:
					#forecast = forecastio.load_forecast(forecastio_api_key, loc[0], loc[1], time=gametime) # pull a forecast data block from the API
					forecast = mgr.forecast_at_coords(loc[0], loc[1], '3h')
					#gamecast = forecast.currently() # pull the forecast data from that block for the 'current' time (which is our game time)
					gamecast = forecast.get_weather_at(gametime)
					t = gamecast.temperature('fahrenheit')
					locstr = 'at Great American Ballpark' if row['location'] == "cin" else 'in {}'.format(loc[2])
					data = { 'time': row['time'], 'cast': gamecast.status.lower(), 'temp': round(t["temp"]), 'location': locstr, 'team': teams[row['opponent']][3] } 
					status = 'Forecast for today\'s {time} gametime is {cast} and {temp}F {location} vs the {team}.'.format(**data)
					twitter = TwitterAPI()					
					twitter.tweet(status)
					break
