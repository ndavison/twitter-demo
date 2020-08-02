from argparse import ArgumentParser
from .get_tweets_api import GetTweetsAPI
from .render_tweets import RenderTweets
from .http_server import HTTPServer
from .exceptions import FailedToGetTweetsException
import asyncio

app_description = '''
Monitors a Twitter account for tweet activity. On execution, the 5 most recent
tweets are displayed, and every 10 minutes new activity is displayed.
'''


def get_parser():
    parser = ArgumentParser(description=app_description)
    parser.add_argument(
        '-u',
        '--user',
        required=True,
        help='The value of the Twitter username to retrieve tweets from.'
    )
    # it's unclear whether retweets should be returned from the requirements
    # given, so the -r argument allows you to enable RT's (off by default).
    parser.add_argument(
        '-r',
        '--retweets',
        action='store_true',
        help='Show retweets.'
    )
    # the 'simple curl command' friendly API requirement is enabled by this
    # argument, which establishes an aiohttp server when enabled (off by
    # default). The requirements didn't specify HTTP, and curl has access
    # to a lot of protocols in most its standard OS compilations such as
    # file:// or a unix socket like the Docker daemon API, but HTTP was chosen
    # for its 'most obvious choice' properties.
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
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

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
