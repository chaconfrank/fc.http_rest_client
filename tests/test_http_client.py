import unittest
import requests_mock

from http_rest_client.http_client import HttpClient, HttpMethods


class HttpClientTest(unittest.TestCase):

    def test_get_request(self):
        with requests_mock.Mocker() as mocker:
            mocker.get('https://api.example.com/users', status_code=200)
            client = HttpClient('https://api.example.com')
            response = client.send_request(HttpMethods.GET, '/users')

            self.assertEqual(response.status_code, 200)
