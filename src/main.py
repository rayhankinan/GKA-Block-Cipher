from KeyExpansion import KeyExpansion
from RoundFunction import RoundFunction
from FeistelNetwork import FeistelNetwork
from Constants import NUMBER_OF_ITERATION, BYTES_LENGTH
from OperationMode import OperationMode

if __name__ == "__main__":
    key_expansion = KeyExpansion(b"abcefghijklmnopq")
    round_function = RoundFunction()
    feistel_network = FeistelNetwork(round_function, key_expansion)

    mode_code = "ECB"
    mode = int(input("Choose mode:\n1. ECB\n2. CBC\n3. CFB\n4. OFB\n5. CTR\n"))

    if(mode == 1):
        mode_code = "ECB"
    elif(mode == 2):
        mode_code = "CBC"
    elif(mode == 3):
        mode_code = "CFB"
    elif(mode == 4):
        mode_code = "OFB"
    elif(mode == 5):
        mode_code = "CTR"
    else:
        print("Invalid mode")
    

    content = input("Input content: ").encode()

    if (len(content) % BYTES_LENGTH != 0):
        content += b' ' * (BYTES_LENGTH - (len(content) % BYTES_LENGTH))
    
    iv = b'abcdefghijklmnop'
    if(mode_code == "CTR"):
        iv = b'abcdefghijklmnop'[:BYTES_LENGTH//2]
    elif(mode_code == "ECB"):
        iv = b''

    cipher = OperationMode(mode_code, iv, feistel_network)

    encrypted = cipher.encrypt(content, NUMBER_OF_ITERATION)
    decrypted = cipher.decrypt(encrypted, NUMBER_OF_ITERATION)


    print("Content: ", content)
    print("Encrypted: ", encrypted)
    print("Decrypted: ", decrypted)
