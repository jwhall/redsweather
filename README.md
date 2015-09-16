# redsweather
A Twitter bot that posts the weather forecast for Cincinnati Reds baseball games

# about
This is a small project I did to help learn Python. The code is awful and should be used by nobody, ever. It was an experiment to help figure out how to tie several different open source Python libraries together, to make something useful. Well, useful to Reds fans.

# install
This is written for Python 3. You need a few libraries to make this work:
- Python-Forecastio, from https://github.com/ZeevG/python-forecast.io
- Tweepy, from https://github.com/tweepy/tweepy

You will also need a CSV of your team's schedule. Check out 2015.csv for an example of what the columns should look like. I got mine from http://cincinnati.reds.mlb.com/schedule/downloadable.jsp?c_id=cin#csv-format, your team probably has something similar.

You will need API keys for Twitter and Forecast.io. The python-forecastio Github page has great instructions on getting one for Forecast.io, and I used this blog post - http://videlais.com/2015/03/02/how-to-create-a-basic-twitterbot-in-python/ - to learn how to set up Twitter's OAuth (and also their code to post w/tweepy).

# use
Run once a day for best results. Note that Twitter won't let you post the same status twice, so you will get a 403 upon trying to run the script a second time.
