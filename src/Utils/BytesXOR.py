def bytes_xor(a: bytes, b: bytes) -> bytes:
    return bytes([a[i] ^ b[i] for i in range(len(a))])