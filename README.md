# Twitter demo

This python app monitors a Twitter account for tweet activity, using the asyncio library to create an event loop for the life of the running app. On execution, the 5 most recent tweets are displayed, and every 10 minutes new tweet activity is displayed. The app also includes an inbuilt HTTP API to retrieve all displayed tweets so far.

## setup

This demo requires Python 3 (tested on Python 3.7.5). To install the dependencies:

```
pip install -r requirements.txt
```

## cli

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

## Run as a Docker container

To run this as a Docker container, first build the image from the app's root directory:

```
sudo docker build -t twitterdemo .
```

And then run the container, passing in the Twitter username you want to monitor as the first argument:

```
sudo docker run --rm -p 9000:9000 twitterdemo tinycarebot
```

This also runs the HTTP server on port 9000.