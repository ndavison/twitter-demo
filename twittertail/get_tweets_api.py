from twittertail.get_twitter_values import GetTwitterValues
from twittertail.exceptions import (
    FailedToGetTwitterValueException,
    FailedToGetTweetsException
)
from html import unescape
import requests
import re


class GetTweetsAPI:
    '''
    GetTweetsAPI mimmicks the process a browser uses when accessing a Twitter
    user's tweet timeline in an unauthenticated session. To do this, it:

    1. Gets the "guest token" from the Twitter markup, and uses it in the
    "x-guest-token" request header in the API call.

    2. Gets the bearer token from the Twitter main.js, and uses it in the
    "authorization" request header in the API call.

    3. Gets the user id for the supplied username from a GraphQL query.

    4. Queries the Twitter API at /2/timeline/profile/X.json, where X is the
    user id.

    Arguments:
        user (str): the username of the Twitter user to query against.
        retweets (bool): toggles whether to return retweets

    Raises:
        FailedToGetTweetsException: if the username is invalid by Twitter
        standards.
    '''

    def __init__(self, user, retweets=False):
        if len(user) > 15 or re.search('[^a-zA-Z0-9_]+', user):
            raise FailedToGetTweetsException(
                'Invalid username - Twitter usernames must be 15 or fewer '
                'characters in length, and must be alphanumeric only '
                '(with underscores).'
            )
        self.user = user
        self.retweets = retweets
        self.__refresh_twitter_values()
        self.s_twitter = requests.session()
        self.headers = {
            'x-guest-token': self.gt,
            'authorization': 'Bearer %s' % (self.bearer_token),
            'content-type': 'application/json'
        }
        self.user_id = self.__get_user_id()

    def __refresh_twitter_values(self):
        (
            self.gt,
            self.bearer_token,
            self.query_id
        ) = self.__get_new_twitter_values()

    def __get_new_twitter_values(self):
        '''
        Collect the values needed to make an unauthenticated request to the
        Twitter API for a user's timeline, using GetTwitterValues.

        Raises:
            FailedToGetTweetsException: if values could not be retrieved.

        Return:
            gt, bearer_token, query_id (tuple): the API values.
        '''

        twitter_values = GetTwitterValues()
        try:
            gt = twitter_values.get_guest_token()
            bearer_token = twitter_values.get_bearer_token()
            query_id = twitter_values.get_query_id()
        except FailedToGetTwitterValueException as e:
            raise FailedToGetTweetsException(e)
        return (gt, bearer_token, query_id)

    def get_twitter_values(self):
        '''
        Returns the current tokens retrieved from Twitter.

        Returns:
            tuple: the guest token, bearer token, and query id
        '''

        return (self.gt, self.bearer_token, self.query_id)

    def __get_user_id(self):
        '''
        Gets the id of the Twitter username supplied, by querying the GraphQL
        API's "UserByScreenName" operation.

        Raises:
            FailedToGetTweetsException: if the user id could not be retrieved.

        Returns:
            user_id (str): the user id.
        '''
        user_id = None
        url = (
            'https://api.twitter.com/graphql/%s/UserByScreenName'
            % (self.query_id)
        )
        params = {
            'variables': (
                '{"screen_name":"%s","withHighlightedLabel":true}'
                % (self.user)
            )
        }
        try:
            r = self.s_twitter.get(
                url,
                params=params,
                headers=self.headers
            )
            graph_ql_json = r.json()
        except Exception as e:
            raise FailedToGetTweetsException(
                'Failed to get the user id, request excepted with: %s'
                % (str(e))
            )
        try:
            user_id = graph_ql_json['data']['user']['rest_id']
        except KeyError:
            raise FailedToGetTweetsException(
                'Failed to get the user id, could not find user rest_id in '
                'GraphQL response.'
            )
        return user_id

    def get_tweets(
        self,
        count=None,
        refresh_tokens=False,
        last_id=None
    ):
        '''
        Queries the Twitter API using a guest token and authorization bearer
        token retrived from GetTwitterValues().

        Arguments:
            count (int): the amount of tweets to get.
            refresh_tokens (bool): get new tokens before checking for tweets.
            last_id (int): the id of the latest seen tweet.

        Raises:
            FailedToGetTweetsException: if tweets could not be retrieved.

        Returns:
            tweets (list): a list of tweet timestamp and text tuples for the
                user, sorted ascending in time, limited by the 'limit'
                argument.
        '''

        if refresh_tokens:
            self.__refresh_twitter_values()

        tweets = list()

        try:
            url = (
                'https://api.twitter.com/2/timeline/profile/%s.json'
                % self.user_id
            )
            # the 'count' param in this query is actually a maximum,
            # where deleted or suspended tweets are removed after the
            # count is applied, so we don't supply a count param in
            # the API query and instead apply it to the response data
            # later.
            params = {
                'tweet_mode': 'extended'
            }
            r = self.s_twitter.get(url, headers=self.headers, params=params)
            timeline_json = r.json()
        except Exception as e:
            raise FailedToGetTweetsException(
                'Failed to get tweets, request excepted with: %s'
                % (str(e))
            )
        try:
            tweets_json = timeline_json['globalObjects']['tweets']
            if self.retweets:
                tweet_ids = list(int(x) for x in tweets_json.keys())
            else:
                tweet_ids = list(
                    int(x) for x in tweets_json.keys()
                    if 'retweeted_status_id_str' not in tweets_json[x]
                )
            # if a last id value is supplied, only return tweets which an id
            # greater
            if last_id:
                tweet_ids = list(x for x in tweet_ids if x > last_id)
            if len(tweet_ids) > 0:
                # an assumption here is the display should be oldest to newest,
                # i.e. opposite to Twitter's UI, as it makes more sense in a
                # cli environment.
                tweet_ids.sort(reverse=True)
                tweet_ids_culled = tweet_ids[:count]
                tweet_ids_culled.sort()
                tweets = (
                    list(
                        (
                            tweets_json[str(x)]['created_at'],
                            unescape(tweets_json[str(x)]['full_text']),
                            tweets_json[str(x)]['id_str']
                        )
                        for x in tweet_ids_culled
                    )
                )
        except KeyError:
            raise FailedToGetTweetsException('Failed to get tweets.')
        return tweets
