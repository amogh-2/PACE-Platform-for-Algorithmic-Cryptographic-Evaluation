from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

def encrypt_file_aes_cbc(file):
    try:
        key = os.urandom(16)  # AES_cbc-128 key (16 bytes)
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
    
def decrypt_file_aes_cbc(filepath, key_b64, iv_b64):
    try:
        key = base64.b64decode(key_b64)
        iv = base64.b64decode(iv_b64)

        with open(filepath, 'rb') as file:
            encrypted_data = file.read()

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        pad_length = decrypted_data[-1]
        decrypted_data = decrypted_data[:-pad_length]

        decrypted_filepath = filepath.replace(".enc", ".dec")
        with open(decrypted_filepath, 'wb') as file:
            file.write(decrypted_data)

        return decrypted_filepath
    except Exception as e:
        raise Exception(f"Decryption failed: {str(e)}")