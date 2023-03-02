from Constants import FIRST_PRIME, SECOND_PRIME, LARGE_PRIME, PRIMITIVE_ROOT, SUBSTITUTION_BIT, MULTIPLIER_LCG, INCREMENT_LCG, MODULUS_LCG


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


def generate_list_bbs(seed: int, n: int) -> list[int]:
    # Blum-Blum-Shub Pseudo-Random Number Generator (Key Expansion)
    m = FIRST_PRIME * SECOND_PRIME

    list_of_random_int = [seed]
    for i in range(n):
        list_of_random_int.append(
            binary_exponentiation(list_of_random_int[i], 2, m)
        )

    return list_of_random_int[1:]


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

def generate_list_lcg(seed: int, n = SUBSTITUTION_BIT) -> list[int]:
    # Linear Congruential Generator (create s-box)
    list_of_random_int = [seed]
    for i in range(n - 1):
        list_of_random_int.append(
            (list_of_random_int[i] * MULTIPLIER_LCG + INCREMENT_LCG) % MODULUS_LCG
        )

    return list_of_random_int


def generate_permutation(content: bytes, seed: int) -> bytes:
    # Fisher-Yates Shuffle Algorithm (Round Function)
    arr = bytearray(content)
    length = len(content)
    random_int = generate_list_bm(seed, length)

    for i in range(length - 1, 0, -1):
        j = random_int[i] % (i + 1)
        arr[i], arr[j] = arr[j], arr[i]

    return bytes(arr)
