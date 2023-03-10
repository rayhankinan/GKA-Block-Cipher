import sys
from typing import Callable
from Constants.CipherOperation import SUBSTITUTION_BIT
from Utils import shuffle_bytes, substitute_bytes


class RoundFunction:
    def __init__(self) -> None:
        # TODO: Definisikan inner state untuk round function jika dibutuhkan
        pass

    def hash_function(self, key: bytes, content: bytes) -> bytes:
        # TODO: Definisikan hash function yang invertible
        int_internal_key = int.from_bytes(key, sys.byteorder)

        return shuffle_bytes(substitute_bytes(content, int_internal_key), int_internal_key)

    def get_hash(self, key: bytes) -> Callable[[bytes], bytes]:
        return lambda content: self.hash_function(key, content)
