from KeyExpansion import KeyExpansion
from RoundFunction import RoundFunction
from FeistelNetwork import FeistelNetwork
from Constants import NUMBER_OF_ITERATION

from Utils import shuffle_bits, unsuffle_bits
import sys

if __name__ == "__main__":
    key_expansion = KeyExpansion(b"abcefghijklmnopq")
    round_function = RoundFunction()
    feistel_network = FeistelNetwork(round_function, key_expansion)
    content = b"kinankerenbanget"

    # encrypted = feistel_network.encrypt(content, NUMBER_OF_ITERATION)
    # decrypted = feistel_network.decrypt(encrypted, NUMBER_OF_ITERATION)

    # print("Content: ", content)
    # print("Encrypted: ", encrypted)
    # print("Decrypted: ", decrypted)

    int_external_key = int.from_bytes(
        key_expansion.get_external_key(),
        sys.byteorder,
    )

    shuffled = shuffle_bits(content, int_external_key)
    print()

    unshuffled = unsuffle_bits(shuffled, int_external_key)
