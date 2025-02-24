import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.backends import default_backend

def decrypt_file_chacha20(filepath, key_b64, nonce_b64):
    """Decrypts a file using ChaCha20 with a base64-encoded key and nonce."""
    
    # Decode base64-encoded key and nonce
    key = base64.b64decode(key_b64)
    nonce = base64.b64decode(nonce_b64)

    # Read encrypted data from the file
    with open(filepath, 'rb') as file:
        encrypted_data = file.read()

    # Create cipher
    algorithm = algorithms.ChaCha20(key, nonce)
    cipher = Cipher(algorithm, mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Decrypt the data
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Save decrypted file
    decrypted_filepath = filepath.replace(".enc", ".dec")  # Change extension for output file
    with open(decrypted_filepath, 'wb') as file:
        file.write(decrypted_data)

    return decrypted_filepath