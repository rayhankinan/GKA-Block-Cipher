import sys
from RoundFunction import RoundFunction
from KeyExpansion import KeyExpansion
from Utils import bytes_xor, generate_permutation, generate_inverse_permutation


class FeistelNetwork:
    def __init__(self, round_function: RoundFunction, key_expansion: KeyExpansion) -> None:
        self.round_function = round_function
        self.key_expansion = key_expansion

    def encrypt(self, content: bytes, num_of_iteration: int):
        external_key = self.key_expansion.get_external_key()
        int_external_key = int.from_bytes(external_key, sys.byteorder)

        permutated_content = generate_permutation(content, int_external_key)
        iterated_content = self.iterated_encrypt(
            permutated_content,
            num_of_iteration,
        )
        inverse_permutated_content = generate_inverse_permutation(
            iterated_content,
            int_external_key,
        )

        return inverse_permutated_content

    def iterated_encrypt(self, content: bytes, num_of_iteration: int, current_index: int = 0) -> bytes:
        if current_index == num_of_iteration:
            return content

        else:
            length = len(content)
            left, right = content[:length // 2], content[length // 2:]

            internal_key = self.key_expansion.get_internal_key(current_index)
            hash = self.round_function.get_hash(internal_key)

            left, right = right, bytes_xor(left, hash(right))

            return self.iterated_encrypt(left + right, num_of_iteration, current_index + 1)

    def decrypt(self, content: bytes, num_of_iteration: int):
        external_key = self.key_expansion.get_external_key()
        int_external_key = int.from_bytes(external_key, sys.byteorder)

        permutated_content = generate_permutation(content, int_external_key)
        iterated_content = self.iterated_decrypt(
            permutated_content,
            num_of_iteration,
        )
        inverse_permutated_content = generate_inverse_permutation(
            iterated_content,
            int_external_key,
        )

        return inverse_permutated_content

    def iterated_decrypt(self, content: bytes, num_of_iteration: int, current_index: int = 0) -> bytes:
        if current_index == num_of_iteration:
            return content

        else:
            length = len(content)
            left, right = content[:length // 2], content[length // 2:]

            internal_key = self.key_expansion.get_internal_key(
                num_of_iteration - current_index - 1
            )
            hash = self.round_function.get_hash(internal_key)

            left, right = bytes_xor(right, hash(left)), left

            return self.iterated_decrypt(left + right, num_of_iteration, current_index + 1)
