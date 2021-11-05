import asyncio
import os
import random
from urllib.parse import urljoin
from typing import Any, Union, List
import sys

import httpx

from visionpy.defaults import DEFAULT_TIMEOUT, DEFAULT_API_KEYS
from visionpy.version import VERSION


class AsyncHTTPProvider(object):
    """An Async HTTP Provider for API request.

    :params endpoint_uri: HTTP API URL base.
        Default value is ``"https://visionexplorer.bkbos.space/"``. Can also be configured via
        the ``VISIONPY_HTTP_PROVIDER_URI`` environment variable.
    """

    def __init__(
        self,
        endpoint_uri: Union[str, dict] = None,
        timeout: float = DEFAULT_TIMEOUT,
        client: httpx.AsyncClient = None,
        api_key: Union[str, List[str]] = None,
    ):
        super().__init__()

        if endpoint_uri is None:
            self.endpoint_uri = os.environ.get("VISIONPY_HTTP_PROVIDER_URI", "https://visionexplorer.bkbos.space/")
        elif isinstance(endpoint_uri, (dict,)):
            self.endpoint_uri = endpoint_uri["fullnode"]
        elif isinstance(endpoint_uri, (str,)):
            self.endpoint_uri = endpoint_uri
        else:
            raise TypeError("unknown endpoint uri {}".format(endpoint_uri))

        if 'visiongrid' in self.endpoint_uri:
            self.use_api_key = True
            if isinstance(api_key, (str,)):
                self._api_keys = [api_key]
            elif isinstance(api_key, (list,)) and api_key:
                self._api_keys = api_key
            else:
                self._api_keys = DEFAULT_API_KEYS.copy()

            self._default_api_keys = self._api_keys.copy()
        else:
            self.use_api_key = False

        headers = {"User-Agent": f"Visionpy/{VERSION}"}
        if client is None:
            self.client = httpx.AsyncClient(headers=headers, timeout=httpx.Timeout(timeout))
        else:
            self.client = client

        self.timeout = timeout
        """Request timeout in second."""

    async def make_request(self, method: str, params: Any = None) -> dict:
        if self.use_api_key:
            self.client.headers["Vision-Pro-Api-Key"] = self.random_api_key

        if params is None:
            params = {}
        url = urljoin(self.endpoint_uri, method)
        resp = await self.client.post(url, json=params)
        if self.use_api_key:
            if resp.status_code == 403 and b'Exceed the user daily usage' in resp.content:
                print("W:", resp.json().get('Error', 'rate limit!'), file=sys.stderr)
                self._handle_rate_limit()
                return await self.make_request(method, params)

        resp.raise_for_status()
        return resp.json()

    async def make_get_request(self, method: str, params: Any = None) -> dict:
        if params is None:
            params = {}
        url = urljoin(self.endpoint_uri, method)
        resp = await self.client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    @property
    def random_api_key(self):
        return random.choice(self._api_keys)

    def _handle_rate_limit(self):
        if len(self._api_keys) > 1:
            self._api_keys.remove(self.client.headers["Vision-Pro-Api-Key"])
        else:
            print("W: Please add as-many API-Keys in HTTPProvider", file=sys.stderr)
            asyncio.sleep(0.9)
