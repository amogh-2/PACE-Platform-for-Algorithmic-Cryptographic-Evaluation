from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
import os
import base64

def encrypt_file_chacha20_poly1305(file):
    try:
        key = os.urandom(32)  # 256-bit key for ChaCha20-Poly1305
        nonce = os.urandom(12)  # 12-byte nonce

        chacha = ChaCha20Poly1305(key)

        file_data = file.read()
        encrypted_data = chacha.encrypt(nonce, file_data, None)
        
        return {
            "encrypted_data": base64.b64encode(encrypted_data).decode(),
            "key": base64.b64encode(key).decode(),
            "nonce": base64.b64encode(nonce).decode(),
        }
    except Exception as e:
        return {"error": f"Encryption failed: {str(e)}"}