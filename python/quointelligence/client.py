"""
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
"""

import logging
import re
from typing import Dict, Optional, Tuple, Generator
import requests
import os

from dateutil import parser as dateparser
from datetime import datetime, timezone, timedelta
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError
from requests.packages.urllib3.util.retry import Retry

logger = logging.getLogger(__file__)


def _datetime_str_to_utc(s):
    try:
        d = dateparser.isoparse(s).astimezone(timezone.utc)
    except ValueError:
        raise ValueError("date string `%s` is not formatted properly" % s)
    return d.isoformat(timespec="seconds").split("+", 1)[0]


class QIClient:
    DEFAULT_URL = "https://api.quointelligence.eu/v0.1"
    LOGIN_PATH = "/login"
    DRP_PATH = "/drp"
    INTELLIGENCE_PATH = "/intelligence"
    SERVICE_REQUESTS_PATH = "/service-requests"
    TICKET_PATH = "/ticket/%d"

    def __init__(self, email=None, password=None, cert=None, url=None):
        """
        Build a new client. Configure by setting parameters, or by environment
        variable:
            QI_API_EMAIL          Client account email address
            QI_API_PASSWORD       Client password
            QI_API_URL            (if using other than the default URL)
            QI_API_CLIENT_CERT    (if needed, path to client SSL certificate)
        """

        # Parse configuration
        try:
            email = email or os.environ["QI_API_EMAIL"]
            password = password or os.environ["QI_API_PASSWORD"]
            cert = cert or os.environ.get("QI_API_CLIENT_CERT", None)

            self._url: str = (
                url or os.environ.get("QI_API_URL", self.DEFAULT_URL)
            ).strip("/")
        except KeyError as e:
            raise ValueError(
                "Must specify parameter or define environment variable %s" % e
            )

        if not self._url.startswith("https://") and not self._url.startswith(
            "http://localhost"
        ):
            raise ValueError("API url must specify https://")

        # Create http session
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)
        http.cert = cert
        self._http = http

        # Login and get authentication token
        self._token = None
        response = self._http.post(
            self._url + self.LOGIN_PATH,
            json={"email": email, "password": password},
            headers=self._headers(),
        )
        try:
            response.raise_for_status()
        except HTTPError:
            raise ValueError("Authentication failure")

        self._token = response.json()["access_token"]

    def _headers(self) -> Dict[str, str]:
        """Provide standard request headers"""

        headers = dict()
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json"
        if self._token:
            headers["Authorization"] = "Bearer %s" % self._token

        return headers

    def _parse_dates(
        self, since: Optional[str] = None, date_range: Optional[Tuple[str, str]] = None
    ) -> Dict[str, str]:
        """Provide standard parsing of date filters"""

        if since and date_range:
            raise ValueError("Either specify since or date_range, not both")

        if since is not None:
            if (m := re.match(r"(\d+)m", since)) is not None:
                delta = timedelta(minutes=int(m.group(1)))
            elif (m := re.match(r"(\d+)h", since)) is not None:
                delta = timedelta(hours=int(m.group(1)))
            elif (m := re.match(r"(\d+)d", since)) is not None:
                delta = timedelta(days=int(m.group(1)))
            else:
                raise ValueError(
                    "`since` is not formatted properly: %s. Example: 2d: 2 days. 1h: 1 hour, 3m: 3 minutes"
                    % since
                )

            return {
                "since": (datetime.utcnow() - delta).isoformat(timespec="seconds"),
            }

        if date_range is not None:
            since, until = date_range
            return {
                "since": _datetime_str_to_utc(since),
                "until": _datetime_str_to_utc(until),
            }

        return {}  # no filter

    def _query_endpoint(
        self,
        path: str,
        since: Optional[str] = None,
        date_range: Optional[Tuple[str, str]] = None,
        params: Optional[Dict[str, any]] = None,
    ) -> Generator[dict, None, None]:
        """Provide standard filtering/querying of an endpoint"""

        if params is None:
            params = {}

        params.update(self._parse_dates(since, date_range))
        params["page_start"] = 0

        logger.debug("Querying %s with parameters (%s)", path, params)

        while True:
            response = self._http.get(
                self._url + path, params=params, headers=self._headers()
            )

            if response.status_code == 204:  # End of results?
                break

            try:
                response.raise_for_status()
            except HTTPError:
                raise ValueError(
                    "Error occurred accessing %s: %s" % (path, response.text)
                )

            tickets = response.json()

            if len(tickets) == 0:  # End of results? (alternate method)
                break

            yield from tickets

            params["page_start"] += len(tickets)

    def drp(
        self,
        since: Optional[str] = None,
        date_range: Optional[Tuple[str, str]] = None,
        params: Optional[Dict[str, any]] = None,
    ) -> Generator[dict, None, None]:
        """
        Query brand protection tickets

        examples:
        tickets = client.drp(since='1h')   # 1 hour
        tickets = client.drp(since='15m')  # 15 minutes
        tickets = client.drp(since='40d')  # 40 days
        tickets = client.drp(date_range=('2020-10-01', '2021-04-07'))
        """
        yield from self._query_endpoint(self.DRP_PATH, since, date_range, params)

    def intelligence(
        self,
        since: Optional[str] = None,
        date_range: Optional[Tuple[str, str]] = None,
        params: Optional[Dict[str, any]] = None,
    ) -> Generator[dict, None, None]:
        """
        Query intelligence tickets

        examples:
        tickets = client.intelligence(since='1h')   # 1 hour
        tickets = client.intelligence(since='15m')  # 15 minutes
        tickets = client.intelligence(since='40d')  # 40 days
        tickets = client.intelligence(date_range=('2020-10-01', '2021-04-07'))
        """
        yield from self._query_endpoint(
            self.INTELLIGENCE_PATH, since, date_range, params
        )

    def service_requests(
        self,
        since: Optional[str] = None,
        date_range: Optional[Tuple[str, str]] = None,
        params: Optional[Dict[str, any]] = None,
    ) -> Generator[dict, None, None]:
        """
        Query service request tickets

        examples:
        tickets = client.service_requests(since='1h')   # 1 hour
        tickets = client.service_requests(since='15m')  # 15 minutes
        tickets = client.service_requests(since='40d')  # 40 days
        tickets = client.service_requests(date_range=('2020-10-01', '2021-04-07'))
        """
        yield from self._query_endpoint(
            self.SERVICE_REQUESTS_PATH, since, date_range, params
        )

    def ticket(self, id) -> dict:
        """Get extended ticket details given a ticket id"""

        logger.debug("Fetching ticket (%d)", id)

        response = self._http.get(
            self._url + (self.TICKET_PATH % int(id)), headers=self._headers()
        )

        try:
            response.raise_for_status()
        except HTTPError:
            raise ValueError("Error occurred fetching ticket")

        return response.json()
