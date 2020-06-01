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
        metadata = self._handler.get_metadata()
        # handlers can change url e.g redirect
        self._url = self._handler._url
        return metadata

    def get_content(self):
        metadata = self.get_metadata()
        fileobj = self._handler.get_fileobj()

        content_analyzer = ContentAnalyzer(self._url, fileobj, metadata["type"])
        metadata.update(content_analyzer.get_content())

        return metadata
