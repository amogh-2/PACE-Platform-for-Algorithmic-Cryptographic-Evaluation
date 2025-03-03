import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

def decrypt_file_aes_gcm(filepath, key_b64, nonce_b64, tag_b64):
    try:
        
        try:
            key = base64.b64decode(key_b64)
            nonce = base64.b64decode(nonce_b64)
            tag = base64.b64decode(tag_b64) if tag_b64 else None
            
            
            if len(key) not in [16, 24, 32]:
                raise ValueError(f"Invalid key length: {len(key)} bytes. Must be 16, 24, or 32 bytes.")
            
            
            if len(nonce) != 12:
                raise ValueError(f"Invalid nonce length: {len(nonce)} bytes. Must be 12 bytes.")
        except Exception as e:
            raise ValueError(f"Invalid key, nonce, or tag format: {str(e)}")

        with open(filepath, 'rb') as file:
            encrypted_data = file.read()
        
        
        if tag:
            
            ciphertext = encrypted_data
        else:
       
            ciphertext = encrypted_data[:-16]
            tag = encrypted_data[-16:]

       
        aesgcm = AESGCM(key)
        
        try:
          
            decrypted_data = aesgcm.decrypt(nonce, ciphertext + (tag if tag else b''), None)
        except Exception as e:
            raise ValueError(f"Decryption failed, possibly due to incorrect key, nonce, or tag: {str(e)}")

        decrypted_filepath = filepath.replace(".enc", ".dec")
        with open(decrypted_filepath, 'wb') as file:
            file.write(decrypted_data)

        return decrypted_filepath
    except Exception as e:
        raise Exception(f"Decryption failed: {str(e)}")

