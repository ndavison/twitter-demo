# Twitter demo

## setup

This demo requires Python 3 (tested on Python 3.7.5). To install the dependencies:

```
pip install -r requirements.txt
```

## cli

This monitors a Twitter account for tweet activity. On execution, the 5 most recent tweets are displayed, and every 10 minutes new activity is displayed. The app will run indefinitely - you can kill the app with CTRL+C.

The cli program can be run like so:

```
python tweets.py -u TWITTER_USERNAME
```

See `-h` for more options.

[![asciicast](https://asciinema.org/a/XSoCw81l7iErqygL0NVBatdgQ.png)](https://asciinema.org/a/XSoCw81l7iErqygL0NVBatdgQ)

## HTTP

By passing in a `-w` argument, a simple HTTP server will run, allowing you to query the tweets collected so far as in a JSON array.

```
python tweets.py -u TWITTER_USERNAME -w
```

Get tweets via:

```
curl http://127.0.0.1:9000/tweets
```