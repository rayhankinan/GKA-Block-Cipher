from Constants import FIRST_PRIME, SECOND_PRIME, LARGE_PRIME, PRIMITIVE_ROOT


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
    m = FIRST_PRIME * SECOND_PRIME

    list_of_random_int = [seed]
    for i in range(n):
        list_of_random_int.append(
            binary_exponentiation(list_of_random_int[i], 2, m)
        )

    return list_of_random_int[1:]


def generate_list_bm(seed: int, n: int) -> list[int]:
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


def generate_number_bbs(seed: int, index: int) -> int:
    exponent = binary_exponentiation(
        2, index + 1, lcm((FIRST_PRIME - 1) * (SECOND_PRIME - 1))
    )
    result = binary_exponentiation(seed, exponent, FIRST_PRIME * SECOND_PRIME)

    return result
