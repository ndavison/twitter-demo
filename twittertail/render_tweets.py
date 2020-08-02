from colored import fg, attr
from twittertail.exceptions import FailedToGetTweetsException
import asyncio
import sys


class RenderTweets:
    def get_tweets(
        self,
        tweets_response,
        count=None,
        refresh_tokens=False,
        last_id=None
    ):
        '''
        Gets the tweets from the GetTweetsAPI() instance.

        Arguments:
            tweets_response: the GetTweetsAPI() instance.
            count (int): the amount of tweets to return.
            refresh_tokens (bool): get new tokens before checking for tweets.
            last_id (int): the id of the latest seen tweet.

        Return:
            tweets_api (list): the tweets retrieved from GetTweetsAPI().
        '''

        tweets_api = list()
        try:
            tweets_api = tweets_response.get_tweets(
                count=count,
                refresh_tokens=refresh_tokens,
                last_id=last_id
            )
        except FailedToGetTweetsException as e:
            print(e)
            exit(1)
        return tweets_api

    def render_tweets(self, tweets):
        '''
        Prints out the tweets to stdout.

        Arguments:
            tweets (list): the list of tweet tuples to print.
        '''

        for tweet in tweets:
            # remove newlines in each tweet, so newlines differentiate between
            # tweets in the output
            sys.stdout.write(
                '[%s %s %s] %s\n'
                % (fg(111), tweet[0], attr(0), ' '.join(tweet[1].splitlines()))
            )
            sys.stdout.flush()

    async def render_5_most_recent_tweets(self, tweets, tweets_response):
        '''
        Gets the 5 most recent tweets and renders them.

        Arguments:
            tweets (list): the tweets to render.
            tweets_response: the GetTweetsAPI() instance.
        '''

        tweets += self.get_tweets(tweets_response, count=5)
        self.render_tweets(tweets)

    async def render_new_tweets_every_10_minutes(
        self,
        tweets,
        tweets_response
    ):
        '''
        Sets a loop to retrieve unseen tweets, checking every 10 minutes.

        Arguments:
            tweets (list): the tweets to render.
            tweets_response: the GetTweetsAPI() instance.
        '''

        while True:
            await asyncio.sleep(10 * 60)
            last_id = int(tweets[-1][2])
            new_tweets = self.get_tweets(
                tweets_response,
                count=None,
                refresh_tokens=True,
                last_id=last_id
            )
            self.render_tweets(new_tweets)
            if new_tweets:
                tweets += new_tweets
