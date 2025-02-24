from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

def encrypt_file_aes(file):
    try:
        key = os.urandom(16)  # AES-128 key (16 bytes)
        iv = os.urandom(16)   # IV (16 bytes)
        
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        file_data = file.read()
        padded_data = file_data + b' ' * (16 - len(file_data) % 16)  # PKCS7 padding
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        return {
            "encrypted_data": base64.b64encode(encrypted_data).decode(),
            "key": base64.b64encode(key).decode(),
            "iv": base64.b64encode(iv).decode(),
        }
    except Exception as e:
        return {"error": f"Encryption failed: {str(e)}"}