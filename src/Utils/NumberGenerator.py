import math
import sys
from Constants import FIRST_PRIME, SECOND_PRIME, SUBSTITUTION_BIT, PRIMITIVE_ROOT, LARGE_PRIME


def binary_exponentiation(a: int, b: int, m: int) -> int:
    if a == 0:
        return 0
    if b == 0:
        return 1

    y = 0
    if b % 2 == 0:
        y = binary_exponentiation(a, b // 2, m)
        y = (y * y) % m

    else:
        y = a % m
        y = (y * binary_exponentiation(a, b - 1, m) % m) % m

    return ((y + m) % m)


def gcd(a: int, b: int) -> int:
    if b == 0:
        return a

    return gcd(b, a % b)


def lcm(a: int, b: int) -> int:
    return (a * b) // gcd(a, b)


def generate_number_bbs(seed: int, index: int) -> int:
    # Blum-Blum-Shub Pseudo-Random Number Generator (Key Expansion)
    exponent = binary_exponentiation(
        2, index + 1, lcm((FIRST_PRIME - 1), (SECOND_PRIME - 1))
    )
    result = binary_exponentiation(seed, exponent, FIRST_PRIME * SECOND_PRIME)

    return result


def generate_list_bm(seed: int, n: int) -> list[int]:
    # Blum-Micali Pseudo-Random Number Generator (Round Function)
    list_of_random_int = [seed]
    for i in range(n):
        list_of_random_int.append(
            binary_exponentiation(
                PRIMITIVE_ROOT,
                list_of_random_int[i],
                LARGE_PRIME
            )
        )

    return list_of_random_int[1:]


def generate_permutation(content: bytes, seed: int) -> bytes:
    # Fisher-Yates Shuffle Algorithm (Round Function)
    arr = bytearray(content)
    length = len(content)
    random_int = generate_list_bm(seed, length)

    for i in range(length - 1, 0, -1):
        j = random_int[i] % (i + 1)
        arr[i], arr[j] = arr[j], arr[i]

    return bytes(arr)


def generate_inverse_permutation(content: bytes, seed: int) -> bytes:
    # TODO: Implement this
    pass


def generate_substitution(content: bytes, seed: int) -> bytes:
    # Fisher-Yates Shuffle Algorithm (Round Function)
    arr = bytearray(content)
    length = len(content)

    random_int = generate_list_bm(seed, SUBSTITUTION_BIT)
    s_box = [i for i in range(SUBSTITUTION_BIT)]
    s_box_size = int(math.sqrt(SUBSTITUTION_BIT))

    for i in range(SUBSTITUTION_BIT - 1, 0, -1):
        j = random_int[i] % (i + 1)
        s_box[i], s_box[j] = s_box[j], s_box[i]

    for i in range(length):
        left, right = arr[i] >> 4, arr[i] & 0x0F

        new_int = s_box[left * s_box_size + right] % SUBSTITUTION_BIT
        arr[i] = new_int

    return bytes(arr)
