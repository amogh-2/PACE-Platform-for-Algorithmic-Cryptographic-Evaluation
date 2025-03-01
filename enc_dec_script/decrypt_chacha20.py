import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def decrypt_file_chacha20(filepath, key_b64, nonce_b64):
    try:
        # Validate key and nonce
        try:
            key = base64.b64decode(key_b64)
            nonce = base64.b64decode(nonce_b64)
            
            # Validate key length (must be 32 bytes for ChaCha20)
            if len(key) != 32:
                raise ValueError(f"Invalid key length: {len(key)} bytes. Must be 32 bytes.")
            
            # Validate nonce length (must be 16 bytes for ChaCha20)
            if len(nonce) != 16:
                raise ValueError(f"Invalid nonce length: {len(nonce)} bytes. Must be 16 bytes.")
        except Exception as e:
            raise ValueError(f"Invalid key or nonce format: {str(e)}")

        with open(filepath, 'rb') as file:
            encrypted_data = file.read()

        # Create ChaCha20 cipher
        algorithm = algorithms.ChaCha20(key, nonce)
        cipher = Cipher(algorithm, mode=None, backend=default_backend())
        decryptor = cipher.decryptor()
        
        try:
            # Decrypt the data
            decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        except Exception as e:
            raise ValueError(f"Decryption failed, possibly due to incorrect key or nonce: {str(e)}")

        decrypted_filepath = filepath.replace(".enc", ".dec")
        with open(decrypted_filepath, 'wb') as file:
            file.write(decrypted_data)

        return decrypted_filepath
    except Exception as e:
        raise Exception(f"Decryption failed: {str(e)}")

