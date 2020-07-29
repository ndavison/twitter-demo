from argparse import ArgumentParser
from src.get_tweets_api import GetTweetsAPI
from src.render_tweets import RenderTweets
from src.http_server import HTTPServer
from src.exceptions import FailedToGetTweetsException
import asyncio

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
parser.add_argument(
    '-i',
    '--interface',
    default='0.0.0.0',
    help='The interface to run the HTTP server on. Defaults to 0.0.0.0.'
)
parser.add_argument(
    '-p',
    '--port',
    default=9000,
    help='The port to run the HTTP server on. Defaults to 9000.'
)

args = parser.parse_args()

if not args.user:
    print('You must supply a user value, use -h for help.')
    exit(1)

# the asyncio event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

tweets = list()
try:
    tweets_response = GetTweetsAPI(
        user=args.user,
        retweets=args.retweets
    )
except FailedToGetTweetsException as e:
    print(e)
    exit(1)
renderer = RenderTweets()

# if the HTTP API is enabled, start an async web server
if args.web_server:
    http_server = HTTPServer()
    http_server.start_server(loop, args.interface, args.port, tweets)

task = loop.create_task(
    renderer.render_5_most_recent_tweets(tweets, tweets_response)
)
loop.run_until_complete(task)
task = loop.create_task(
    renderer.render_new_tweets_every_10_minutes(
        tweets,
        tweets_response
    )
)

try:
    loop.run_forever()
except (KeyboardInterrupt, SystemExit):
    loop.close()
    exit(0)
