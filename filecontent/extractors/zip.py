import os
from zipfile import ZipFile
from tempfile import TemporaryDirectory
from pathlib import Path
from ..content import ContentAnalyzer


class Extractor:

    needs_file = True

    @staticmethod
    def match(filename, type_hint):
        path = Path(filename)
        if "/zip" in type_hint or path.suffix == ".zip":
            return True
        return False

    def __init__(self, filename):
        self._filename = filename

    def get_content(self):

        files = []
        with ZipFile(self._filename, "r") as zip_file:
            for member_info in zip_file.infolist():
                if member_info.is_dir():
                    continue
                with TemporaryDirectory() as tmp_dir:
                    extracted_fname = zip_file.extract(member_info, tmp_dir)
                    with open(extracted_fname, "rb") as extracted_file:
                        file_content = ContentAnalyzer(
                            extracted_fname, extracted_file, hide_path=tmp_dir + os.sep
                        )
                        files.append(file_content.get_content())

        return files
