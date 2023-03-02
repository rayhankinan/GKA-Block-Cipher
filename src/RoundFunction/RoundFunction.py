import sys
from typing import Callable
from Utils import bytes_xor, generate_permutation, generate_list_lcg


class RoundFunction:
    def __init__(self) -> None:
        # TODO: Definisikan inner state untuk round function jika dibutuhkan
        pass

    def hash_function(self, key: bytes, content: bytes) -> bytes:
        # TODO: Definisikan hash function yang invertible
        int_internal_key = int.from_bytes(key, sys.byteorder)
        s_box = generate_list_lcg(int_internal_key)
        # substitute each byte in content with the corresponding byte in s_box
        content = bytearray(content)
        for i in range(len(content)):
            left, right = content[i] >> 4, content[i] & 0x0F
            new_int = s_box[left*16 + right] % 256
            newbyte = new_int.to_bytes(1, sys.byteorder)
            content[i] = newbyte[0]

        return generate_permutation(content, int_internal_key)

    def get_hash(self, key: bytes) -> Callable[[bytes], bytes]:
        return lambda content: self.hash_function(key, content)
