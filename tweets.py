from argparse import ArgumentParser
from src.get_tweets_api import GetTweetsAPI
from src.exceptions import FailedToGetTweetsException
from src.util import render_tweets
from aiohttp import web
import json
import requests
import time
import asyncio
import threading

app_description = '''
Monitors a Twitter account for tweet activity. On execution, the 5 most recent
tweets are displayed, and every 10 minutes new activity is displayed.
'''

parser = ArgumentParser(description=app_description)
parser.add_argument(
    '-u',
    '--user',
    help='The value of the Twitter username to retrieve tweets from.'
)
parser.add_argument(
    '-r',
    '--retweets',
    action='store_true',
    help='Show retweets.'
)
parser.add_argument(
    '-w',
    '--web-server',
    action='store_true',
    help='Run a simple HTTP server to get the tweets collected so far.'
)
parser.add_argument('-v', '--verbose', action='store_true', help='More output.')

args = parser.parse_args()

if not args.user:
    print('You must supply a user value, use -h for help.')
    exit(1)

def get_tweets(count=None, new_only=False, refresh_tokens=False):
    tweets_api = list()
    try:
        tweets_api = tweets_response.get_tweets(
            count=count,
            new_only=new_only,
            refresh_tokens=refresh_tokens
        )
        if args.verbose:
            gt, bearer_token, query_id = tweets_response.get_twitter_values()
            print('Using guest token "%s" and bearer token "%s"\n' % (gt, bearer_token))
    except FailedToGetTweetsException as e:
        print(e)
        exit(1)
    return tweets_api

async def render_5_most_recent_tweets(tweets):
    tweets += get_tweets(count=5)
    render_tweets(tweets)

async def render_new_tweets_every_10_minutes(tweets):
    while True:
        await asyncio.sleep(10 * 60)
        if args.verbose:
            print('Checking for new tweets...')
        new_tweets = get_tweets(count=None, new_only=True, refresh_tokens=True)
        render_tweets(new_tweets)
        if new_tweets:
            tweets += new_tweets

def http_server():
    async def http_tweets(request):
        tweets_json = list({'created_at': x[0], 'full_text': x[1]} for x in tweets)
        return web.Response(
            body=json.dumps(tweets_json),
            headers={
                'content-type': 'application/json'
            }
        )
    app = web.Application()
    app.router.add_get('/tweets', http_tweets)
    runner = web.AppRunner(app)
    return runner

# the asyncio event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# if the HTTP API is enabled, start an async web server
if args.web_server:
    runner = http_server()
    loop.run_until_complete(runner.setup())
    server = web.TCPSite(runner, 'localhost', 9000)
    loop.run_until_complete(server.start())

tweets = list()
tweets_response = GetTweetsAPI(
    user=args.user,
    retweets=args.retweets
)

task = loop.create_task(render_5_most_recent_tweets(tweets))
loop.run_until_complete(task)
task = loop.create_task(render_new_tweets_every_10_minutes(tweets))

try:
    loop.run_forever()
except (KeyboardInterrupt, SystemExit):
    exit(0)
