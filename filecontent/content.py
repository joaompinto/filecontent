from tempfile import NamedTemporaryFile
from functools import partial
from hashlib import sha512


class ContentAnalyzer:
    def __init__(self, filename: str, fileobj: object, type_hint: str = None):
        self._filename = filename
        self._fileobj = fileobj
        self._type_hint = type_hint
        self._extractor = None
        self._tmp_file = None
        self._size = 0
        self._sha512 = sha512()
        print("HINT", type_hint)

        content_type = None
        if self._type_hint:
            if "/zip" in self._type_hint:
                content_type = "zip"

        if content_type == "zip":
            self._tmp_file = NamedTemporaryFile()
            from .extractors import ZipExtractor

            self._extractor = ZipExtractor(self._tmp_file.name)

    def feed(self, content):
        if isinstance(content, str):
            content = content.encode()
        self._sha512.update(content)
        if self._tmp_file:
            self._tmp_file.write(content)
        self._size += len(content)

    def get_content(self):
        """ Return content summary """

        part_read = partial(self._fileobj.read, 1024 * 1024)
        iterator = iter(part_read, b"")

        for index, block in enumerate(iterator, start=1):
            self.feed(block)
            if len(block) == 0:
                break
        self._fileobj.close()

        content = {}
        content["name"] = self._filename
        content["size"] = self._size
        content["sha512"] = self._sha512.hexdigest()
        if self._extractor:
            content["files"] = self._extractor.get_content()
        if self._tmp_file:
            self._tmp_file.close()
        return content
