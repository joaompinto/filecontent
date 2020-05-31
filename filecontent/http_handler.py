import requests
from gzip import GzipFile


class HTTPHandler:
    def __init__(self, url):
        self._url = url

    def get_metadata(self):
        response = requests.head(self._url, allow_redirects=True)
        metadata = {
            "type": response.headers["content-type"],
            "date": response.headers["date"],
            "size": int(response.headers.get("content-length", "0")),
        }
        return metadata

    def get_fileobj(self):
        response = requests.get(self._url, stream=True, allow_redirects=True)
        if response.headers.get("content-encoding") == "gzip":
            return GzipFile(fileobj=response.raw)
        else:
            return response.raw
