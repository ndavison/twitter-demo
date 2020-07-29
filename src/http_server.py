from aiohttp import web
import json


class HTTPServer:
    def start_server(self, loop, interface, port, tweets):
        '''
        Starts the aiohttp server on the supplied interface and port.

        Arguments:
            loop: the asyncio event loop.
            interface (string): the interface to listen on.
            port (int): the port to listen on.
            tweets (list): the list of tweets to return.
        '''

        runner = self.___http_server(tweets)
        loop.run_until_complete(runner.setup())
        server = web.TCPSite(runner, interface, int(port))
        loop.run_until_complete(server.start())

    def ___http_server(self, tweets):
        '''
        Establishes the endponts and HTTP server configuration.

        Arguments:
            tweets (list): the list of tweets to return.

        Returns:
            runner: the app runner for asyncio.
        '''

        async def http_tweets(request):
            tweets_json = list(
                {
                    'created_at': x[0],
                    'full_text': x[1],
                    'id': x[2]
                }
                for x in tweets
            )
            return web.Response(
                body=json.dumps({'tweets': tweets_json}),
                headers={
                    'content-type': 'application/json'
                }
            )
        app = web.Application()
        app.router.add_get('/tweets', http_tweets)
        runner = web.AppRunner(app)
        return runner
