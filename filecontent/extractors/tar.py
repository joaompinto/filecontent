from tarfile import TarFile


class Extractor:

    needs_file = True
    match_content = "x-tar"

    def __init__(self, metadata, fileobj):
        # Open a stream of tar blocks for reading with transparent compression.
        self._tarfile = TarFile.open(fileobj=fileobj, mode="r|*")

    def get_content(self):
        for member in self._tarfile.getmembers():
            print(member)

        files = []

        return files
