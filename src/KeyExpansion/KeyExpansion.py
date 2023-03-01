import sys
from Constants import BYTES_LENGTH
from Utils import generate_number_bbs


class KeyExpansion:
    def __init__(self, external_key: bytes) -> None:
        self.external_key = external_key

    def get_internal_key(self, index: int) -> bytes:
        int_external_key = int.from_bytes(self.external_key, sys.byteorder)
        int_internal_key = generate_number_bbs(int_external_key, index)
        truncated_internal_key = int_internal_key % (1 << (BYTES_LENGTH * 8))

        return truncated_internal_key.to_bytes(BYTES_LENGTH, sys.byteorder)
