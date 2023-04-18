from flask import Flask, jsonify, request
from KeyExpansion import KeyExpansion
from RoundFunction import RoundFunction
from FeistelNetwork import FeistelNetwork
from OperationMode import OperationMode
from Constants import NUMBER_OF_ITERATION
import base64

class GKACipher:
    def __init__(self, key):
        self.key_expansion = KeyExpansion(key)
        self.round_function = RoundFunction()
        self.feistel_network = FeistelNetwork(self.round_function, self.key_expansion)
        self.cipher = OperationMode("CBC", key, self.feistel_network)

    def encrypt(self, message):
        return self.cipher.encrypt(message, NUMBER_OF_ITERATION)
    
    def decrypt(self, message):
        return self.cipher.decrypt(message, NUMBER_OF_ITERATION)

app = Flask(__name__)

@app.route('/')
def health_check():
    return 'OK'

@app.route('/encrypt', methods=['POST'])
def encrypt():
    request.get_json()
    key = request.json['key']
    message = request.json['message']
    key = key.encode()
    message = message.encode()
    cipher = GKACipher(key)
    encrypted = cipher.encrypt(message)
    encrypted = base64.b64encode(encrypted)
    encrypted = encrypted.decode()
    return jsonify(ciphertext=encrypted)

@app.route('/decrypt', methods=['POST'])
def decrypt():
    key = request.form['key']
    message = request.form['message']
    message = base64.b64decode(message)
    key = key.encode()
    cipher = GKACipher(key)
    decrypted = cipher.decrypt(message)
    decrypted =  decrypted.decode()
    return jsonify(ciphertext=decrypted)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)