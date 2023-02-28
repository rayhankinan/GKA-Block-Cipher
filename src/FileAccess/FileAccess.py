class FileAccess:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def read(self) -> bytes:
        file = open(self.filename, "rb")
        content = file.read()
        file.close()

        return content

    def write(self, content: bytes) -> None:
        file = open(self.filename, "wb")
        file.write(content)
        file.close()
