from argparse import ArgumentParser
from app.get_tweets_api import GetTweetsAPI
from app.exceptions import FailedToGetTweetsException
import requests

app_description = '''
Monitors a Twitter account for tweet activity. On execution, the 5 most recent
tweets are displayed, and every 10 minutes new activity is displayed.
'''

parser = ArgumentParser(description=app_description)
parser.add_argument(
    "-u",
    "--user",
    help="The value of the Twitter username to retrieve tweets from."
)

args = parser.parse_args()

if not args.user:
    print('You must supply a user value, use -h for help.')
    exit(1)

try:
    tweets_response = GetTweetsAPI(user=args.user)
    tweets = tweets_response.get_tweets(count=5)
    for tweet in tweets:
        print(tweet)
except FailedToGetTweetsException as e:
    print(e)
    exit(1)
