from argparse import ArgumentParser
from src.get_tweets_api import GetTweetsAPI
from src.exceptions import FailedToGetTweetsException
import requests
import re

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

if len(args.user) > 15 or re.search('[^a-zA-Z0-9_]+', args.user):
    print(
        'Invalid username - Twitter usernames must be 15 or few characters in length, and must be alphanumeric only (with underscores).'
    )
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

for tweet in tweets:
    # remove newlines in each tweet, so newlines differentiate between tweets
    # in the output
    print(' '.join(tweet.splitlines()))
