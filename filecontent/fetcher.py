from urllib.parse import urlparse
from hashlib import sha512
from functools import partial
from .http_handler import HTTPHandler


SCHEME_HANDLER = {"http": HTTPHandler, "https": HTTPHandler}


class Fetcher:
    def __init__(self, url: str):
        self._url = url
        self._urlparts = urlparse(url)
        self._scheme = self._urlparts.scheme

    def get_metadata(self):
        """ get the file metadata """
        self._handler = SCHEME_HANDLER[self._scheme](self._url)
        return self._handler.get_metadata()

    def get_sha512_size(self):
        content_sha512 = sha512()
        fileobj = self._handler.get_fileobj()

        part_read = partial(fileobj.read, 1024 * 1024)
        iterator = iter(part_read, b"")
        size = 0
        for index, block in enumerate(iterator, start=1):
            size += len(block)
            content_sha512.update(block)

        return content_sha512.hexdigest(), size

    def get_summary(self):
        summary = self.get_metadata()
        sha512, size = self.get_sha512_size()
        summary.update({"sha512": sha512, "size": size})
        return summary
