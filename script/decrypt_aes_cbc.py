import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
#import os

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