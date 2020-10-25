from bs4 import BeautifulSoup
from twittertail.exceptions import (
    FailedToGetMainJsException,
    FailedToGetTwitterValueException
)
import re
import requests


class GetTwitterValues:
    '''
    GetTwitterValues handles retrieving values from the Twitter markup that
    the frontend uses to query the Twitter API without authentication, such
    as the guest token and the authorization bearer token.
    '''

    def __init__(self):
        self.main_js = self.__get_main_js()

    def __get_main_js(self):
        '''
        Gets the contents of the 'main.XXXX.js' file that Twitter is currently
        using in its markup.

        Raises:
            FailedToGetMainJsException: if the main.XXXX.js file can't be
            retrived.

        Return:
            r.text (str): the contents of the main.XXXX.js file.
        '''
        main_js_href = ''
        try:
            r = requests.get('https://twitter.com')
        except Exception as e:
            raise FailedToGetMainJsException(
                'Failed to find the main.XXXX.js file, request excepted '
                'with: %s'
                % (str(e))
            )
        soup = BeautifulSoup(r.text, 'html.parser')
        for script in soup.find_all(
            href=re.compile(r'responsive-web/[^\/]+/main\.[^\.]+\.js$')
        ):
            main_js_href = script['href']
        if not main_js_href or not main_js_href.startswith('https://'):
            raise FailedToGetMainJsException(
                'Failed to find the main.XXXX.js file'
            )
        try:
            r = requests.get(main_js_href)
        except Exception as e:
            raise FailedToGetMainJsException(
                'Failed to get the main.XXXX.js contents, request excepted '
                'with: %s'
                % (str(e))
            )
        return r.text

    def get_query_id(self):
        '''
        Extracts the GraphQL query id for the 'UserByScreenName' op from the
        Twitter markup. This is set in a JS file which is sourced into the
        main Twitter markup.

        Raises:
            FailedToGetTwitterValueException: if the user id can't be retrived

        Return:
            query_id (str): the query id
        '''

        query_id = ''
        query_id_pattern = re.compile(
            '.*queryId:"([^"]+)",operationName:"UserByScreenName",'
            'operationType:"query".*'
        )
        matches = re.match(query_id_pattern, self.main_js)
        if matches:
            query_id = matches.group(1)
        if not query_id:
            raise FailedToGetTwitterValueException(
                'Failed to get the user GraphQL query id from the Twitter '
                'markup.'
            )
        return query_id

    def get_bearer_token(self):
        '''
        Extracts the "bearer token" from the Twitter markup for use in
        unauthenticated API requests. This is set in a JS file which is
        sourced into the main Twitter markup.

        Raises:
            FailedToGetTwitterValueException: if the token can't be retrieved

        Returns:
            bearer_token (str): the bearer token value
        '''

        bearer_token = ''
        # we assume this pattern will apply to all future tokens.
        token_pattern = re.compile('.*="(AAAA[^"]+).*')
        matches = re.match(token_pattern, self.main_js)
        if matches:
            bearer_token = matches.group(1)
        if not bearer_token:
            raise FailedToGetTwitterValueException(
                'Failed to get the bearer token from the Twitter markup.'
            )
        return bearer_token

    def get_guest_token(self):
        '''
        Extracts the "guest token" from the Twitter markup for use in
        unauthenticated API requests. This is set in an inline JS block.

        Raises:
            FailedToGetTwitterValueException: if the token can't be retrieved

        Returns:
            gt (str): the guest token value
        '''

        gt = ''
        try:
            r = requests.get('https://twitter.com')
        except Exception as e:
            raise FailedToGetTwitterValueException(
                'Failed to find the guest token, request excepted with: %s'
                % (str(e))
            )
        soup = BeautifulSoup(r.text, 'html.parser')
        for script in soup.find_all('script'):
            if 'gt=' in str(script):
                pattern = re.compile('.*gt=([^;]+);.*', re.DOTALL)
                matches = re.match(pattern, str(script))
                if matches:
                    gt = matches.groups(1)[0]
        if not gt:
            raise FailedToGetTwitterValueException(
                'Failed to find the guest token in Twitter markup.'
            )
        return gt
