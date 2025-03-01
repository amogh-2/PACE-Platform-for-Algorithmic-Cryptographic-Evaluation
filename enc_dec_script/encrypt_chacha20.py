from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.backends import default_backend
import os
import base64

def encrypt_file_chacha20(file):
    try:
        key = os.urandom(32)  # 32-byte key for ChaCha20
        nonce = os.urandom(16)  # 16-byte nonce for ChaCha20

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
        return {"error": f"Encryption failed: {str(e)}"}
    
def decrypt_file_chacha20(filepath, key_b64, nonce_b64):
    try:
        key = base64.b64decode(key_b64)
        nonce = base64.b64decode(nonce_b64)

        with open(filepath, 'rb') as file:
            encrypted_data = file.read()

        algorithm = algorithms.ChaCha20(key, nonce)
        cipher = Cipher(algorithm, mode=None, backend=default_backend())
        decryptor = cipher.decryptor()
        
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        decrypted_filepath = filepath.replace(".enc", ".dec")
        with open(decrypted_filepath, 'wb') as file:
            file.write(decrypted_data)

        return decrypted_filepath
    except Exception as e:
        raise Exception(f"Decryption failed: {str(e)}")