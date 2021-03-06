'''
Copyright 2021 QuoIntelligence GmbH
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    https://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import logging
import re
import requests

from dateutil import parser as dateparser
from datetime import datetime, timezone, timedelta
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

logger = logging.getLogger(__file__)

API_URL = 'https://api.quointelligence.eu'


def _datetime_str_to_utc(s):
    try:
        d = dateparser.isoparse(s)
    except ValueError:
        raise ValueError('date string `%s` is not formatted properly' % s)
    return d.astimezone(
        timezone.utc).isoformat(timespec='seconds').split('+', 1)[0]


class QIClient:

    def __init__(self, email, password):
        '''
        Instantiate a client given Mercury credentials
        '''

        if type(email) is not str:
            raise TypeError('email should be a string')
        if type(password) is not str:
            raise TypeError('password should be a string')

        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)
        self._http = http

        # check redirect (only one is expected)
        self._url = API_URL
        response = requests.get(f'{self._url}/docs', allow_redirects=False)
        if response.status_code in (301, 302):
            self._url = response.headers.get('location')[:-5]
            logger.debug('Changed url to %s based on %d redirect',
                         self._url, response.status_code)

        response = self._http.post(
            '%s/login' % self._url,
            json={
                'email': email,
                'password': password
            },
            verify=False,
            headers={'Content-type': 'application/json'})

        if response.status_code // 100 != 2:
            raise ValueError('Received http error on authentication: %d %s' % (
                response.status_code, response.text))

        self._token = response.json()['access_token']

    def _query_endpoint(self, endpoint, since, date_range, qparams=None):

        assert endpoint in ('intelligence', 'drp', 'service-requests')

        if date_range is not None and since is not None:
            raise ValueError('Either specify since or date_range, not both')

        until = None
        if date_range is not None:
            if type(date_range) is not tuple:
                raise TypeError('date_range should be a tuple')
            if len(date_range) != 2:
                raise ValueError('date_range should contain 2 dates')

            since, until = date_range
            since = _datetime_str_to_utc(since)
            until = _datetime_str_to_utc(until)
        elif since is not None:
            match = re.match(r'([1-9]\d*)([mhd])', since)
            if match is None:
                example = '2d: 2 days. 1h: 1 hour, 3m: 3 minutes'
                raise ValueError(
                    '`since` is not formatted properly: %s. Example: %s' % (
                        since, example))
            value = int(match.group(1))
            unit = match.group(2)
            unit2arg = {
                'm': 'minutes',
                'h': 'hours',
                'd': 'days',
            }
            args = {unit2arg[unit]: value}
            delta = timedelta(**args)
            since = (datetime.utcnow() - delta).isoformat(timespec='seconds')
            until = datetime.utcnow().isoformat(timespec='seconds')

        url = self._url + '/' + endpoint

        logger.debug('About to query %s with date range (%s, %s)',
                     url, since, until)

        tickets = []

        if qparams is None:
            qparams = {}
        if until is not None:
            qparams['since'] = since
            qparams['until'] = until
        while True:
            qparams['page_start'] = len(tickets)
            response = self._http.get(
                url, params=qparams, verify=False,
                headers={
                    'Content-type': 'application/json',
                    'Authorization': 'Bearer %s' % self._token
                    })
            if response.status_code // 100 != 2:
                raise Exception('HTTP error occured %s' % response.text)
            t = response.json()
            tickets += t
            if len(t) == 0:
                break
        return tickets

    def drp(self, since=None, date_range=None):
        '''
        Query brand protection tickets

        examples:
        tickets = client.drp(since='1h')   # 1 hour
        tickets = client.drp(since='15m')  # 15 minutes
        tickets = client.drp(since='40m')  # 40 days
        tickets = client.drp(date_range=('2020-10-01', '2021-04-07'))
        '''
        return self._query_endpoint('drp', since, date_range)

    def ticket(self, id):
        '''
        Get ticket details given the ticket id
        '''
        id = int(id)
        response = self._http.get(
            '%s/ticket/%d' % (self._url, id), verify=False,
            headers={
                'Content-type': 'application/json',
                'Authorization': 'Bearer %s' % self._token
                })
        return response.json()
