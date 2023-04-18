from KeyExpansion import KeyExpansion
from RoundFunction import RoundFunction
from FeistelNetwork import FeistelNetwork
from OperationMode import OperationMode
from Constants import NUMBER_OF_ITERATION, BYTES_LENGTH
import time

if __name__ == "__main__":
    key = b"abcdefghijklmnop"
    mode_code = "ECB"
    mode = int(input("Choose mode:\n1. ECB\n2. CBC\n3. CFB\n4. OFB\n5. CTR\n"))

    if mode == 1:
        mode_code = "ECB"
    elif mode == 2:
        mode_code = "CBC"
    elif mode == 3:
        mode_code = "CFB"
    elif mode == 4:
        mode_code = "OFB"
    elif mode == 5:
        mode_code = "CTR"
    else:
        print("Invalid mode")

    content = input("Input content: ").encode()

    key_expansion = KeyExpansion(key)
    round_function = RoundFunction()
    feistel_network = FeistelNetwork(round_function, key_expansion)

    if len(content) % BYTES_LENGTH != 0:
        content += b' ' * (BYTES_LENGTH - (len(content) % BYTES_LENGTH))

    iv = key
    if mode_code == "CTR":
        iv = key[:BYTES_LENGTH // 2]
    elif mode_code == "ECB":
        iv = b''

    cipher = OperationMode(mode_code, iv, feistel_network)

    time_encrypt_start = time.time()
    encrypted = cipher.encrypt(content, NUMBER_OF_ITERATION)
    time_encrypt_end = time.time()

    time_decrypt_start = time.time()
    decrypted = cipher.decrypt(encrypted, NUMBER_OF_ITERATION)
    time_decrypt_end = time.time()

    print("Content: ", content)
    print("Encrypted: ", encrypted)
    print("Time encrypt: ", time_encrypt_end - time_encrypt_start, "s")
    print("Decrypted: ", decrypted)
    print("Time decrypt: ", time_decrypt_end - time_decrypt_start, "s")
