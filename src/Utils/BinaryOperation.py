from typing import Literal


def bytes_xor(a: bytes, b: bytes) -> bytes:
    return bytes([a[i] ^ b[i] for i in range(len(a))])


def access_bit(content: bytes, index: int) -> Literal[0, 1]:
    base = index // 8
    shift = index % 8

    return (content[base] >> shift) & 0x1


def change_bit(content: bytes, index: int, bit: Literal[0, 1]) -> bytes:
    arr = bytearray(content)
    base = index // 8
    shift = index % 8

    if bit == 1:
        arr[base] |= (1 << shift)
    else:
        arr[base] &= ~(1 << shift)

    return bytes(arr)
