from ..RoundFunction import RoundFunction
from ..KeyExpansion import KeyExpansion


class FeistelNetwork:
    def __init__(self, round_function: RoundFunction, key_expansion: KeyExpansion) -> None:
        self.round_function = round_function
        self.key_expansion = key_expansion

    def encrypt(content: bytes) -> bytes:
        pass

    def decrypt(content: bytes) -> bytes:
        pass
