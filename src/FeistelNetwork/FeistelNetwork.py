import sys
from RoundFunction import RoundFunction
from KeyExpansion import KeyExpansion
from Utils import bytes_xor, shuffle_bits, unsuffle_bits


class FeistelNetwork:
    def __init__(self, round_function: RoundFunction, key_expansion: KeyExpansion) -> None:
        self.round_function = round_function
        self.key_expansion = key_expansion

    def encrypt(self, content: bytes, num_of_iteration: int) -> bytes:
        int_external_key = int.from_bytes(
            self.key_expansion.get_external_key(),
            sys.byteorder,
        )

        shuffled = shuffle_bits(content, int_external_key)
        iterated = self.iteration_encrypt(shuffled, num_of_iteration)
        unshuffled = unsuffle_bits(iterated, int_external_key)

        return unshuffled

    def iteration_encrypt(self, content: bytes, num_of_iteration: int, current_index: int = 0) -> bytes:
        if current_index == num_of_iteration:
            return content

        else:
            length = len(content)
            left, right = content[:length // 2], content[length // 2:]

            internal_key = self.key_expansion.get_internal_key(current_index)
            hash = self.round_function.get_hash(internal_key)

            left, right = right, bytes_xor(left, hash(right))

            return self.iteration_encrypt(left + right, num_of_iteration, current_index + 1)

    def decrypt(self, content: bytes, num_of_iteration: int) -> bytes:
        int_external_key = int.from_bytes(
            self.key_expansion.get_external_key(),
            sys.byteorder,
        )

        shuffled = shuffle_bits(content, int_external_key)
        iterated = self.iteration_decrypt(shuffled, num_of_iteration)
        unshuffled = unsuffle_bits(iterated, int_external_key)

        return unshuffled

    def iteration_decrypt(self, content: bytes, num_of_iteration: int, current_index: int = 0) -> bytes:
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

            return self.iteration_decrypt(left + right, num_of_iteration, current_index + 1)
