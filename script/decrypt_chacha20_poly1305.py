import base64
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
#import os

def decrypt_file_chacha20_poly1305(filepath, key_b64, nonce_b64):
    try:
        key = base64.b64decode(key_b64)
        nonce = base64.b64decode(nonce_b64)

        with open(filepath, 'rb') as file:
            encrypted_data = file.read()

        chacha = ChaCha20Poly1305(key)
        decrypted_data = chacha.decrypt(nonce, encrypted_data, None)

        decrypted_filepath = filepath.replace(".enc", ".dec")
        with open(decrypted_filepath, 'wb') as file:
            file.write(decrypted_data)

        return decrypted_filepath
    except Exception as e:
        raise Exception(f"Decryption failed: {str(e)}")