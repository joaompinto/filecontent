from tempfile import NamedTemporaryFile
from functools import partial
from hashlib import sha512
import pkgutil
from importlib import import_module
from filecontent import extractors


class ContentAnalyzer:
    def __init__(
        self, filename: str, fileobj: object, type_hint: str = "", hide_path: str = ""
    ):
        self._filename = filename
        self._fileobj = fileobj
        self._type_hint = type_hint
        self._tmp_file = None
        self._size = 0
        self._sha512 = sha512()
        self._hide_path = hide_path
        self._extractor = self.get_matching_extractor()

    def get_matching_extractor(self):
        for importer, modname, ispkg in pkgutil.iter_modules(extractors.__path__):
            print("Found submodule %s (is a package: %s)" % (modname, ispkg))
            module = import_module(f"filecontent.extractors.{modname}", ".")
            extractor_cls = module.Extractor
            if extractor_cls.match(self._filename, self._type_hint):
                init_parm = self._filename
                # If the filename is remote but the extract needs a file
                # then we must download it to a temporary file
                if ":" in self._filename and extractor_cls.needs_file:
                    self._tmp_file = NamedTemporaryFile()
                    init_parm = self._tmp_file.name
                return extractor_cls(init_parm)
        return None

    def feed(self, content):
        self._sha512.update(content)
        if self._tmp_file:
            self._tmp_file.write(content)
        self._size += len(content)

    def get_content(self):
        """ Return content summary """
        print("get content for", self._filename)

        part_read = partial(self._fileobj.read, 1024 * 1024)
        iterator = iter(part_read, b"")

        print(self._fileobj)
        for index, block in enumerate(iterator, start=1):
            self.feed(block)
            if len(block) == 0:
                break
        self._fileobj.close()

        content = {}
        content["name"] = self._filename[len(self._hide_path) :]
        content["size"] = self._size
        content["sha512"] = self._sha512.hexdigest()

        if self._extractor:
            content["files"] = self._extractor.get_content()
        if self._tmp_file:
            self._tmp_file.close()
        return content
