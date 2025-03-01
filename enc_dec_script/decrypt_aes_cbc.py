import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def decrypt_file_aes_cbc(filepath, key_b64, iv_b64):
    try:
        # Validate key and IV
        try:
            key = base64.b64decode(key_b64)
            iv = base64.b64decode(iv_b64)
            
            # Validate key length (must be 16, 24, or 32 bytes for AES)
            if len(key) not in [16, 24, 32]:
                raise ValueError(f"Invalid key length: {len(key)} bytes. Must be 16, 24, or 32 bytes.")
            
            # Validate IV length (must be 16 bytes for AES-CBC)
            if len(iv) != 16:
                raise ValueError(f"Invalid IV length: {len(iv)} bytes. Must be 16 bytes.")
        except Exception as e:
            raise ValueError(f"Invalid key or IV format: {str(e)}")

        with open(filepath, 'rb') as file:
            encrypted_data = file.read()

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        
        try:
            decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        except Exception as e:
            raise ValueError(f"Decryption failed, possibly due to incorrect key or IV: {str(e)}")

        # Proper PKCS7 padding removal with validation
        try:
            pad_length = decrypted_data[-1]
            
            # Validate padding
            if pad_length > 0 and pad_length <= 16:
                # Check if all padding bytes have the correct value
                padding = decrypted_data[-pad_length:]
                if all(p == pad_length for p in padding):
                    decrypted_data = decrypted_data[:-pad_length]
                else:
                    raise ValueError("Invalid padding detected, possibly due to incorrect key or IV")
            else:
                raise ValueError(f"Invalid padding length: {pad_length}")
        except Exception as e:
            # If padding removal fails, it's likely due to incorrect decryption
            raise ValueError(f"Failed to remove padding, possibly due to incorrect key or IV: {str(e)}")

        decrypted_filepath = filepath.replace(".enc", ".dec")
        with open(decrypted_filepath, 'wb') as file:
            file.write(decrypted_data)

        return decrypted_filepath
    except Exception as e:
        raise Exception(f"Decryption failed: {str(e)}")

