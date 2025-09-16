import pytest
import requests

from config import ApiConfig

class ApiClient:
    def __init__(self):
        self.base_url = ApiConfig.BASE_URL
        self.timeout = ApiConfig.TIMEOUT
        self.headers = ApiConfig.DEFAULT_HEADERS

    def _request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault('timeout', self.timeout)
        kwargs.setdefault('headers', self.headers)

        try:
            response = requests.request(method, url, **kwargs)
            return response
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Request failed: {str(e)}")

    def get(self, endpoint, **kwargs):
        return self._request('GET', endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self._request('POST', endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self._request('PUT', endpoint, **kwargs)

    def patch(self, endpoint, **kwargs):
        return self._request('PATCH', endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self._request('DELETE', endpoint, **kwargs)