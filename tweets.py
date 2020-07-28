from argparse import ArgumentParser
from src.get_tweets_api import GetTweetsAPI
from src.exceptions import FailedToGetTweetsException
from src.util import render_tweets
import requests
import time

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
    help='Show retweets'
)
parser.add_argument('-v', '--verbose', action='store_true', help='More output')

args = parser.parse_args()

if not args.user:
    print('You must supply a user value, use -h for help.')
    exit(1)

try:
    tweets_response = GetTweetsAPI(
        user=args.user,
        retweets=args.retweets
    )
    tweets = tweets_response.get_tweets(count=5)
except FailedToGetTweetsException as e:
    print(e)
    exit(1)

if args.verbose:
    gt, bearer_token, query_id = tweets_response.get_twitter_values()
    print('Using guest token "%s" and bearer token "%s"\n' % (gt, bearer_token))

render_tweets(tweets)

# infinite loop checking for new tweets
while True:
    if args.verbose:
        print('Sleeping for 10 minutes...')
    time.sleep(10)
    if args.verbose:
        print('Checking for new tweets...')
    try:
        tweets = tweets_response.get_tweets(
            new_only=True,
            refresh_tokens=True
        )
        if args.verbose:
            gt, bearer_token, query_id = tweets_response.get_twitter_values()
            print('Using guest token "%s" and bearer token "%s"\n' % (gt, bearer_token))
    except FailedToGetTweetsException as e:
        print(e)
    render_tweets(tweets)
