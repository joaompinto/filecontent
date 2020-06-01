import requests
from gzip import GzipFile


class HTTPHandler:
    def __init__(self, url):
        self._url = url

    def get_metadata(self):
        response = requests.head(self._url, allow_redirects=True)
        response.raise_for_status()
        self._url = response.url  # It maybe different as a result of a redirect
        metadata = {
            "type": response.headers["content-type"],
            "size": int(response.headers.get("content-length", "0")),
            "date": response.headers["date"],
            "etag": response.headers.get("ETag", ""),
        }
        return metadata

    def get_fileobj(self):
        response = requests.get(self._url, stream=True, allow_redirects=True)
        response.raise_for_status()
        if response.headers.get("content-encoding") == "gzip":
            return GzipFile(fileobj=response.raw)
        else:
            return response.raw
