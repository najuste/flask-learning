import requests

from enum import Enum


class ResponseWrapper:
    def __init__(self, success, data=None, error=None):
        self.success = success
        self.data = data
        self.error = error


class RequestMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


def request_handling(request_method, url, **kwargs):
    try:
        response = requests.request(method=request_method.name, url=url, **kwargs)
        response.raise_for_status()
        return ResponseWrapper(success=True, data=response.json())
    except requests.exceptions.HTTPError as error:
        return ResponseWrapper(success=False, error=str(error))
    except requests.exceptions.RequestException as error:
        return ResponseWrapper(success=False, error=str(error))
