from zipfile import ZipFile
from tempfile import TemporaryDirectory
from .content import ContentAnalyzer


class ZipExtractor:
    def __init__(self, filename):
        self._filename = filename

    def get_content(self):

        files = []
        with ZipFile(self._filename, "r") as zip_file:
            for member_info in zip_file.infolist():
                if member_info.is_dir():
                    continue
                print(member_info)
                with TemporaryDirectory() as tmp_dir:
                    extracted_fname = zip_file.extract(member_info, tmp_dir)
                    with open(extracted_fname, "r") as extracted_file:
                        file_content = ContentAnalyzer(
                            member_info.filename, extracted_file
                        )
                        files.append(file_content.get_content())

        return files
