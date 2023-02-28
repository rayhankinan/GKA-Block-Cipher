class OperationMode:
    def __init__(self, content: bytes, external_key: bytes) -> None:
        self.content = content
        self.external_key = external_key
