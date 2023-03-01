from KeyExpansion import KeyExpansion
from RoundFunction import RoundFunction
from FeistelNetwork import FeistelNetwork
from Constants import NUMBER_OF_ITERATION

if __name__ == "__main__":
    key_expansion = KeyExpansion(b"abcefghijklmnopq")
    round_function = RoundFunction()
    feistel_network = FeistelNetwork(round_function, key_expansion)
    content = b"abcefghijklmnopq"

    encrypted = feistel_network.encrypt(content, NUMBER_OF_ITERATION)
    print()
    decrypted = feistel_network.decrypt(encrypted, NUMBER_OF_ITERATION)
    print()

    print("Content: ", content)
    print("Encrypted: ", encrypted)
    print("Decrypted: ", decrypted)
