#import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from kyber_py.kyber.kyber import Kyber  # Import the correct Kyber class
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

# Initialize Kyber instance with the correct parameter set
kyber = Kyber(parameter_set={"k": 2, "eta_1": 3, "eta_2": 2, "du": 10, "dv": 4})

def decrypt_file_kyber_aes(filepath, encrypted_key_b64, secret_key_b64, nonce_b64, tag_b64):
    try:
        # ✅ Decode Base64 inputs
        encrypted_key = base64.b64decode(encrypted_key_b64)
        secret_key = base64.b64decode(secret_key_b64)
        nonce = base64.b64decode(nonce_b64)
        tag = base64.b64decode(tag_b64)

        # ✅ Decrypt shared secret using Kyber KEM
        shared_secret = kyber.decaps(secret_key, encrypted_key)

        # ✅ Use HKDF to derive the AES-256 key from the shared secret
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,  # AES-256 key size
            salt=None,  # Optional: Can set salt for added security
            info=b"Kyber-AES Encryption",
            backend=default_backend()
        )
        aes_key = hkdf.derive(shared_secret)

        # ✅ Read encrypted file data
        with open(filepath, 'rb') as file:
            encrypted_data = file.read()

        # ✅ AES-GCM decryption
        cipher = Cipher(algorithms.AES(aes_key), modes.GCM(nonce, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        # ✅ Save the decrypted file
        decrypted_filepath = filepath.replace(".enc", ".dec")
        with open(decrypted_filepath, 'wb') as file:
            file.write(decrypted_data)

        print(f"✅ File successfully decrypted and saved as: {decrypted_filepath}")
        return decrypted_filepath

    except Exception as e:
        print(f"Decryption failed: {str(e)}")
        return None

# Example Usage
if __name__ == "__main__":
    # Replace with actual encrypted data
    encrypted_key_b64 = "ENCRYPTED_KEY_BASE64"
    secret_key_b64 = "SECRET_KEY_BASE64"
    nonce_b64 = "NONCE_BASE64"
    tag_b64 = "TAG_BASE64"

    encrypted_filepath = "example.txt.enc"  # Replace with actual encrypted file path

    decrypted_file = decrypt_file_kyber_aes(
        encrypted_filepath, encrypted_key_b64, secret_key_b64, nonce_b64, tag_b64
    )
    
    if decrypted_file:
        print(f"Decryption successful: {decrypted_file}")
    else:
        print("Decryption failed!")
