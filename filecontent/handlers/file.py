from os.path import getsize, getmtime
from ..mime import guess_type


class FileHandler:
    def __init__(self, url):
        self._url = url

    def get_metadata(self):
        metadata = {
            "url": self._url,
            "size": getsize(self._url),
            "date": int(getmtime(self._url)),
        }
        guess_type(metadata)
        return metadata

    def get_fileobj(self):
        fileobj = open(self._url, "rb")
        return fileobj
