import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def decrypt_file_aes(filepath, key_b64, iv_b64):
    """Decrypts a file using AES-128 CBC mode with a base64-encoded key and IV."""
    
    # Decode base64-encoded key and IV
    key = base64.b64decode(key_b64)
    iv = base64.b64decode(iv_b64)

    # Read encrypted data from the file
    with open(filepath, 'rb') as file:
        encrypted_data = file.read()

    # Create cipher
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Decrypt the data
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Remove padding (assuming PKCS7 padding was used)
    pad_length = decrypted_data[-1]  # Last byte represents padding length
    decrypted_data = decrypted_data[:-pad_length]

    # Save decrypted file
    decrypted_filepath = filepath.replace(".enc", ".dec")  # Change extension for output file
    with open(decrypted_filepath, 'wb') as file:
        file.write(decrypted_data)

    return decrypted_filepath
