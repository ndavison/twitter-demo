# Twitter demo

## setup

This demo requires Python 3 (tested on Python 3.7.5). To install the dependencies:

```
pip install -r requirements.txt
```

## cli

This monitors a Twitter account for tweet activity. On execution, the 5 most recent tweets are displayed, and every 10 minutes new activity is displayed.

The cli program can be run like so:

```
python tweets.py -u TWITTER_USERNAME
```

See `-h` for more options.

[![asciicast](https://asciinema.org/a/XSoCw81l7iErqygL0NVBatdgQ.png)](https://asciinema.org/a/XSoCw81l7iErqygL0NVBatdgQ)