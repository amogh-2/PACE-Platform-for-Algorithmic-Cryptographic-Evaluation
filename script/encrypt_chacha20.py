from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.backends import default_backend
import os
import base64

def encrypt_file_chacha20(file):
    try:
        key = os.urandom(32)  # 32-byte key for ChaCha20
        nonce = os.urandom(16)  # 12-byte nonce (corrected) 

        print(f"Key (Base64): {base64.b64encode(key).decode()}")  # Debugging
        print(f"Nonce (Base64): {base64.b64encode(nonce).decode()}")  # Debugging

        algorithm = algorithms.ChaCha20(key, nonce)
        cipher = Cipher(algorithm, mode=None, backend=default_backend())
        encryptor = cipher.encryptor()

        file_data = file.read()
        encrypted_data = encryptor.update(file_data) + encryptor.finalize()

        return {
            "encrypted_data": base64.b64encode(encrypted_data).decode(),
            "key": base64.b64encode(key).decode(),
            "nonce": base64.b64encode(nonce).decode()
        }
    except Exception as e:
        print(f"Error: {str(e)}")  # Print actual error
        return {"error": f"Encryption failed: {str(e)}"}
