from ..RoundFunction import RoundFunction
from ..KeyExpansion import KeyExpansion


class FeistelNetwork:
    def __init__(self, round_function: RoundFunction, key_expansion: KeyExpansion) -> None:
        self.round_function = round_function
        self.key_expansion = key_expansion

    def encrypt(self, content: bytes, num_of_iteration: int, current_index: int = 0) -> bytes:
        if current_index == num_of_iteration:
            return content

        else:
            length = len(content)
            left, right = content[:length // 2], content[length // 2:]

            internal_key = self.key_expansion.get_internal_key(current_index)
            hash = self.round_function.get_hash(internal_key)
            left, right = right, left ^ hash(right)

            return self.encrypt(left + right, num_of_iteration, current_index + 1)

    def decrypt(self, content: bytes, num_of_iteration: int, current_index: int = 0) -> bytes:
        if current_index == num_of_iteration:
            return content

        else:
            length = len(content)
            left, right = content[:length // 2], content[length // 2:]

            internal_key = self.key_expansion.get_internal_key(
                num_of_iteration - current_index - 1
            )
            hash = self.round_function.get_hash(internal_key)
            left, right = right, left ^ hash(right)

            return self.decrypt(content, num_of_iteration, current_index + 1)
