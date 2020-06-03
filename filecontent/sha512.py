from hashlib import sha512


class SHA512File:
    def __init__(self, fileobj):
        self._file = fileobj
        self._sha512 = sha512()
        self._size = 0

    def read(self, size=0):
        data = self._file.read(size)
        self._sha512.update(data)
        self._size += len(data)
        return data

    def sha512(self):
        return self._sha512.hexdigest()

    def size(self):
        return self._size

    def close(self):
        self._file.close()
