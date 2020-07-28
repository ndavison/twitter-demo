def render_tweets(tweets):
    for tweet in tweets:
        # remove newlines in each tweet, so newlines differentiate between tweets
        # in the output
        print(' '.join(tweet.splitlines()))
