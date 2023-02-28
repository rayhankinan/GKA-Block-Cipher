class KeyExpansion:
    def __init__(self, external_key: bytes) -> None:
        self.external_key = external_key

    def get_internal_key(self, index: int) -> bytes:
        pass
