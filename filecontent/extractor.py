import pkgutil
from importlib import import_module
from filecontent import extractors
from tempfile import NamedTemporaryFile


class ExtractorManager:
    def __init__(self, metadata: dict, fileobj: object):
        self._metadata = metadata
        self._filename = metadata["url"]
        self._type_hint = metadata["type"]
        self._file_obj = fileobj
        self.tmp_file = None
        self._extractor = None
        self.get_matching_extractor()

    @staticmethod
    def check_match_content(type_hint, extractor_match):
        """ type_hint and extractor_match can be strings or lists """
        if not type_hint:
            return extractor_match is None
        if not extractor_match:
            raise Exception(f"Required parameter {extractor_match}")
        if not isinstance(type_hint, (list, tuple)):
            type_hint = [type_hint]
        if not isinstance(extractor_match, (list, tuple)):
            extractor_match = [extractor_match]
        for match_case in extractor_match:
            for hint in type_hint:
                if match_case in hint:
                    return True
        return False

    def get_matching_extractor(self):
        for importer, modname, ispkg in pkgutil.iter_modules(extractors.__path__):
            module = import_module(f"filecontent.extractors.{modname}", ".")
            extractor_cls = module.Extractor
            match_content = getattr(extractor_cls, "match_content", None)
            if ExtractorManager.check_match_content(self._type_hint, match_content):
                # If the filename is remote but the extract needs a file
                # then we must download it to a temporary file
                if ":" in self._filename and extractor_cls.needs_file:
                    self.tmp_file = NamedTemporaryFile()
                    original_url = self._metadata["url"]
                    # We temporary replace the url with the temp filename
                    self._metadata["url"] = self.tmp_file.name
                    self._extractor = extractor_cls(self._metadata, self._file_obj)
                    self._metadata["url"] = original_url
                else:
                    self._extractor = extractor_cls(self._metadata, self._file_obj)

    def get_content(self, metadata):
        if self._extractor:
            metadata["files"] = self._extractor.get_content()
        return metadata
