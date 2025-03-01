import base64
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
import os

def decrypt_file_chacha20_poly1305(filepath, key_b64, nonce_b64):
    try:
        # Validate key and nonce
        try:
            key = base64.b64decode(key_b64)
            nonce = base64.b64decode(nonce_b64)
            
            # Validate key length (must be 32 bytes for ChaCha20Poly1305)
            if len(key) != 32:
                raise ValueError(f"Invalid key length: {len(key)} bytes. Must be 32 bytes.")
            
            # Validate nonce length (must be 12 bytes for ChaCha20Poly1305)
            if len(nonce) != 12:
                raise ValueError(f"Invalid nonce length: {len(nonce)} bytes. Must be 12 bytes.")
        except Exception as e:
            raise ValueError(f"Invalid key or nonce format: {str(e)}")

        with open(filepath, 'rb') as file:
            encrypted_data = file.read()
        
        # For ChaCha20Poly1305, the tag is the last 16 bytes
        ciphertext = encrypted_data[:-16]
        tag = encrypted_data[-16:]

        # Create ChaCha20Poly1305 object
        chacha = ChaCha20Poly1305(key)
        
        try:
            # Decrypt the data
            # For ChaCha20Poly1305, the tag is verified during decryption
            decrypted_data = chacha.decrypt(nonce, ciphertext + tag, None)
        except Exception as e:
            raise ValueError(f"Decryption failed, possibly due to incorrect key or nonce: {str(e)}")

        decrypted_filepath = filepath.replace(".enc", ".dec")
        with open(decrypted_filepath, 'wb') as file:
            file.write(decrypted_data)

        return decrypted_filepath
    except Exception as e:
        raise Exception(f"Decryption failed: {str(e)}")

