from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

def encrypt_file_aes_gcm(file):
    try:
        key = os.urandom(16)  # AES-128 key (16 bytes)
        nonce = os.urandom(12)  # 96-bit nonce for GCM

        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
        encryptor = cipher.encryptor()

        file_data = file.read()
        encrypted_data = encryptor.update(file_data) + encryptor.finalize()
        
        return {
            "encrypted_data": base64.b64encode(encrypted_data).decode(),
            "key": base64.b64encode(key).decode(),
            "nonce": base64.b64encode(nonce).decode(),
            "tag": base64.b64encode(encryptor.tag).decode(),
        }
    except Exception as e:
        return {"error": f"Encryption failed: {str(e)}"}