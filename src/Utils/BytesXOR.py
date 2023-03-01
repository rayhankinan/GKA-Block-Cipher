import sys
from Constants import BYTES_LENGTH


def bytes_xor(a: bytes, b: bytes) -> bytes:
    int_a = int.from_bytes(a, sys.byteorder)
    int_b = int.from_bytes(b, sys.byteorder)
    int_res = int_a ^ int_b
    truncated_res = int_res % (1 << (BYTES_LENGTH // 2 * 8))

    return truncated_res.to_bytes(BYTES_LENGTH // 2, sys.byteorder)
