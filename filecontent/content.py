from functools import partial
from hashlib import sha512
from .sha512 import SHA512File
from .extractor import ExtractorManager
from .mime import guess_type

READ_CHUNK_SIZE = 1024 * 1024


class ContentAnalyzer:
    def __init__(self, metadata: dict, fileobj: object, hide_path: str = ""):
        guess_type(metadata)
        self._metadata = metadata
        self._filename = metadata["url"]
        self._fileobj = SHA512File(fileobj)
        self._tmp_file = None
        self._sha512 = sha512()
        self._hide_path = hide_path
        self._extractor_manager = ExtractorManager(metadata, fileobj)

    def _read_file_chunks(self):
        """ Read from fileobj fat READ_CHUNK_SIZE chunks """

        part_read = partial(self._fileobj.read, READ_CHUNK_SIZE)
        iterator = iter(part_read, b"")
        for index, content in enumerate(iterator, start=1):
            if self._extractor_manager.tmp_file:
                self._extractor_manager.tmp_file.write(content)
            if len(content) == 0:
                break

    def get_content(self):
        """ Get content summary """

        # Read file at chunks to calculate sha512 sum
        self._read_file_chunks()

        metadata = self._metadata
        metadata["url"] = self._filename[len(self._hide_path) :]
        metadata["size"] = self._fileobj.size()
        metadata["sha512"] = self._fileobj.sha512()

        self._extractor_manager.get_content(metadata)

        self._fileobj.close()
        if self._extractor_manager.tmp_file:
            self._extractor_manager.tmp_file.close()
        return metadata
