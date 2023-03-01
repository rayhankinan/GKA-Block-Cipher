from FeistelNetwork import FeistelNetwork


class OperationMode:
    def __init__(self, content: bytes, external_key: bytes) -> None:
        self.content = content
        self.external_key = external_key

    def encrypt(self, feistel_network: FeistelNetwork) -> bytes:
        raise NotImplementedError()

    def decrypt(self, feistel_network: FeistelNetwork) -> bytes:
        raise NotImplementedError()
