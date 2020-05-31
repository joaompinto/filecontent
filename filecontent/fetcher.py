from urllib.parse import urlparse
from .http_handler import HTTPHandler
from .content import ContentAnalyzer


SCHEME_HANDLER = {"http": HTTPHandler, "https": HTTPHandler}


class Fetcher:
    def __init__(self, url: str):
        self._url = url
        self._urlparse = urlparse(url)
        self._scheme = self._urlparse.scheme
        self._content_analyzer = None

    def get_metadata(self):
        """ get the file metadata """
        self._handler = SCHEME_HANDLER[self._scheme](self._url)
        self._metadata = self._handler.get_metadata()
        return self._metadata

    def get_content(self):
        self.get_metadata()
        fileobj = self._handler.get_fileobj()

        self._content_analyzer = ContentAnalyzer(
            self._url, fileobj, self._metadata["type"]
        )

        return self._content_analyzer.get_content()
