import mimetypes


def guess_type(metadata: dict):
    mime_type, mime_encoding = mimetypes.guess_type(metadata["url"])
    if "type" not in metadata:
        metadata["type"] = mime_type
    if "encoding" not in metadata:
        metadata["encoding"] = mime_encoding
