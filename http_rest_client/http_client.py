from enum import Enum

import requests
from requests import Response


class HttpMethods(Enum):
    GET = 'GET',
    POST = 'POST',
    PUT = 'PUT',
    DELETE = 'DELETE'


class HttpClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}

    @property
    def get_headers(self):
        return self.headers

    def send_request(self, http_method: HttpMethods, endpoint: str, data=None) -> Response:
        url = self.base_url + endpoint

        if http_method == HttpMethods.GET:
            response = requests.get(url, headers=self.get_headers)
        elif http_method == HttpMethods.POST:
            response = requests.post(url, headers=self.get_headers, json=data)
        elif http_method == HttpMethods.PUT:
            response = requests.put(url, headers=self.get_headers, json=data)
        elif http_method == HttpMethods.DELETE:
            response = requests.delete(url, headers=self.get_headers)
        else:
            raise ValueError("Invalid HTTP method")

        return response




