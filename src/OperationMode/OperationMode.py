from FeistelNetwork import FeistelNetwork
from Utils import bytes_xor
from Constants import BYTES_LENGTH


class OperationMode:
    block_size = BYTES_LENGTH

    def __init__(self, mode: str, external_key: bytes, feistel_network: FeistelNetwork) -> None:
        self.mode = mode
        self.external_key = external_key
        self.feistel_network = feistel_network
        if(mode == "CTR"):
            assert(len(external_key) == BYTES_LENGTH//2)
        elif (mode == "ECB"):
            assert(len(external_key) == 0)
        else:
            assert(len(external_key) == BYTES_LENGTH)
            

    def encrypt(self, content: bytes, num_of_iteration: int) -> bytes:
        case = {
            "ECB": self.ecb_encrypt,
            "CBC": self.cbc_encrypt,
            "CFB": self.cfb_encrypt,
            "OFB": self.ofb_encrypt,
            "CTR": self.ctr_encrypt,
        }

        try:
            return case[self.mode](content, num_of_iteration)
        except KeyError:
            return case["ECB"](content, num_of_iteration)


    def decrypt(self, content: bytes, num_of_iteration: int) -> bytes:
        case = {
            "ECB": self.ecb_decrypt,
            "CBC": self.cbc_decrypt,
            "CFB": self.cfb_decrypt,
            "OFB": self.ofb_decrypt,
            "CTR": self.ctr_decrypt,
        }

        try:
            return case[self.mode](content, num_of_iteration)
        except KeyError:
            return case["ECB"](content, num_of_iteration)

    # ECB: Classic Feistel Network
    def ecb_encrypt(self, content: bytes, num_of_iteration: int) -> bytes:
        assert(len(content) % self.block_size == 0)
        result = bytearray()
        for i in range(0, len(content), self.block_size):
            result += self.feistel_network.encrypt(content[i:i+self.block_size], num_of_iteration)
        return bytes(result)
    
    def ecb_decrypt(self, content: bytes, num_of_iteration: int) -> bytes:
        assert(len(content) % self.block_size == 0)
        result = bytearray()
        for i in range(0, len(content), self.block_size):
            result += self.feistel_network.decrypt(content[i:i+self.block_size], num_of_iteration)
        return bytes(result)
    
    # CBC: use external key as IV, and XOR it with the previous block
    def cbc_encrypt(self, content: bytes, num_of_iteration: int) -> bytes:
        assert(len(content) % self.block_size == 0)
        result = bytearray()
        current_xor = self.external_key
        for i in range(0, len(content), self.block_size):
            current_block = bytes_xor(content[i:i+self.block_size], current_xor)
            current_xor = self.feistel_network.encrypt(current_block, num_of_iteration)
            result += current_xor
        return bytes(result)
    
    def cbc_decrypt(self, content: bytes, num_of_iteration: int) -> bytes:
        assert(len(content) % self.block_size == 0)
        result = bytearray()
        current_xor = self.external_key
        for i in range(0, len(content), self.block_size):
            current_block = self.feistel_network.decrypt(content[i:i+self.block_size], num_of_iteration)
            current_xor = bytes_xor(current_block, current_xor)
            result += current_xor
            current_xor = content[i:i+self.block_size]
        return bytes(result)


    # CFB: use external key as IV, Encrypt the IV, and XOR it with the previous block. The encrypted result is then used as IV for the next block
    def cfb_encrypt(self, content: bytes, num_of_iteration: int) -> bytes:
        assert(len(content) % self.block_size == 0)
        result = bytearray()
        current_xor = self.external_key
        for i in range(0, len(content), self.block_size):
            current_block = content[i:i+self.block_size]
            current_xor = self.feistel_network.encrypt(current_xor, num_of_iteration)
            current_xor = bytes_xor(current_xor, current_block)
            result += current_xor
        return bytes(result)
    
    def cfb_decrypt(self, content: bytes, num_of_iteration: int) -> bytes:
        assert(len(content) % self.block_size == 0)
        result = bytearray()
        current_xor = self.external_key
        for i in range(0, len(content), self.block_size):
            current_block = content[i:i+self.block_size]
            current_xor = self.feistel_network.encrypt(current_xor, num_of_iteration)
            current_xor = bytes_xor(current_xor, current_block)
            result += current_xor
            current_xor = current_block
        return bytes(result)
    
    # OFB: the IV is generated independently. The IV is then encrypted, and XORed with the plaintext to generate the ciphertext. The encrypted IV is then used as IV for the next block
    def ofb_encrypt(self, content: bytes, num_of_iteration: int) -> bytes:
        assert(len(content) % self.block_size == 0)
        result = bytearray()
        current_xor = self.external_key
        for i in range(0, len(content), self.block_size):
            current_block = content[i:i+self.block_size]
            current_xor = self.feistel_network.encrypt(current_xor, num_of_iteration)
            result += bytes_xor(current_xor, current_block)
        return bytes(result)
    
    def ofb_decrypt(self, content: bytes, num_of_iteration: int) -> bytes:
        assert(len(content) % self.block_size == 0)
        result = bytearray()
        current_xor = self.external_key
        for i in range(0, len(content), self.block_size):
            current_block = content[i:i+self.block_size]
            current_xor = self.feistel_network.encrypt(current_xor, num_of_iteration)
            result += bytes_xor(current_xor, current_block)
        return bytes(result)
    
    # CTR: use external key as IV, and XOR it with the counter. The counter is the index of the block combined with the external key
    def ctr_encrypt(self, content: bytes, num_of_iteration: int) -> bytes:
        assert(len(content) % self.block_size == 0)
        result = bytearray()
        current_xor = self.external_key
        for i in range(0, len(content), self.block_size):
            current_block = content[i:i+self.block_size]
            counter = i // self.block_size
            counter = counter.to_bytes(self.block_size//2, byteorder='big')
            counter = b"".join([self.external_key, counter])
            current_xor = self.feistel_network.encrypt(counter, num_of_iteration)
            result += bytes_xor(current_xor, current_block)
        return bytes(result)

    def ctr_decrypt(self, content: bytes, num_of_iteration: int) -> bytes:
        assert(len(content) % self.block_size == 0)
        result = bytearray()
        current_xor = self.external_key
        for i in range(0, len(content), self.block_size):
            current_block = content[i:i+self.block_size]
            counter = i // self.block_size
            counter = counter.to_bytes(self.block_size//2, byteorder='big')
            counter = b"".join([self.external_key, counter])
            current_xor = self.feistel_network.encrypt(counter, num_of_iteration)
            result += bytes_xor(current_xor, current_block)
        return bytes(result)