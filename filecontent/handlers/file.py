from mimetypes import guess_type
from os.path import getsize, getmtime


class FileHandler:
    def __init__(self, url):
        self._url = url

    def get_metadata(self):
        filename = self._url
        metadata = {
            "url": filename,
            "type": guess_type(filename),
            "size": getsize(filename),
            "date": int(getmtime(filename)),
        }
        return metadata

    def get_fileobj(self):
        fileobj = open(self._url, "rb")
        return fileobj
