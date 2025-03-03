import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def decrypt_file_chacha20(filepath, key_b64, nonce_b64):
    try:
     
        try:
            key = base64.b64decode(key_b64)
            nonce = base64.b64decode(nonce_b64)
            
           
            if len(key) != 32:
                raise ValueError(f"Invalid key length: {len(key)} bytes. Must be 32 bytes.")
            
          
            if len(nonce) != 16:
                raise ValueError(f"Invalid nonce length: {len(nonce)} bytes. Must be 16 bytes.")
        except Exception as e:
            raise ValueError(f"Invalid key or nonce format: {str(e)}")

        with open(filepath, 'rb') as file:
            encrypted_data = file.read()

       
        algorithm = algorithms.ChaCha20(key, nonce)
        cipher = Cipher(algorithm, mode=None, backend=default_backend())
        decryptor = cipher.decryptor()
        
        try:
            
            decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        except Exception as e:
            raise ValueError(f"Decryption failed, possibly due to incorrect key or nonce: {str(e)}")

        decrypted_filepath = filepath.replace(".enc", ".dec")
        with open(decrypted_filepath, 'wb') as file:
            file.write(decrypted_data)

        return decrypted_filepath
    except Exception as e:
        raise Exception(f"Decryption failed: {str(e)}")

