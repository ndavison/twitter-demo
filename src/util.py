from colored import fg, attr

def render_tweets(tweets):
    for tweet in tweets:
        # remove newlines in each tweet, so newlines differentiate between tweets
        # in the output
        print(
            '[%s %s %s] ' % (fg(111), tweet[0], attr(0)),
            ' '.join(tweet[1].splitlines())
        )
