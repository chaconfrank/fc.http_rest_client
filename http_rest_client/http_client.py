from enum import Enum

import requests
from requests import Response
from requests.exceptions import Timeout

from http_rest_client.auth0_command_handler import Command
from http_rest_client.command_dispatch import Dispatch


class HttpMethods(Enum):
    GET = 'GET',
    POST = 'POST',
    PUT = 'PUT',
    DELETE = 'DELETE'


class HttpClient:
    def __init__(self, base_url, max_tries=1, time_out=100):
        self.tries: int = 0
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}
        self.max_tries = max_tries
        self.time_out = time_out/1000

    @property
    def get_headers(self):
        return self.headers

    @property
    def get_tries(self):
        return self.tries

    def send_request(
            self, http_method: HttpMethods, endpoint: str, data=None, command_auth=None
    ) -> Response | TimeoutError | ValueError:

        self._set_header_authenticate(command_auth)
        url = self.base_url + endpoint

        self.tries = 0
        while self.tries < self.max_tries:
            try:
                if http_method == HttpMethods.GET:
                    return requests.get(url, headers=self.get_headers, timeout=self.time_out)
                elif http_method == HttpMethods.POST:
                    return requests.post(url, headers=self.get_headers, json=data, timeout=self.time_out)
                elif http_method == HttpMethods.PUT:
                    return requests.put(url, headers=self.get_headers, json=data, timeout=self.time_out)
                elif http_method == HttpMethods.DELETE:
                    return requests.delete(url, headers=self.get_headers, timeout=self.time_out)
                else:
                    raise ValueError("Invalid HTTP method")
            except Timeout:
                print(f"Timeout occurred. Retrying ({self.tries + 1}/{self.max_tries})...")
            finally:
                self.tries += 1

        raise Timeout("Maximum number of retries exceeded.")

    def _set_headers(self, key: str, value: str):
        self.headers.setdefault(key, value)

    def _set_header_authenticate(self, command_auth: Command):
        if command_auth:
            token = Dispatch().execute(command_auth)
            self._set_headers('Authorization', token)
