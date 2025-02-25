#import os
import base64
#import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from kyber_py.kyber.kyber import Kyber  # Import the Kyber class
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

# Initialize Kyber
kyber = Kyber(parameter_set={"k": 2, "eta_1": 3, "eta_2": 2, "du": 10, "dv": 4})

def decrypt_file_kyber_aes(filepath, encrypted_key_b64, secret_key_b64, nonce_b64, tag_b64):
    try:
        # ✅ Decode Base64 inputs provided by the user
        encrypted_key = base64.b64decode(encrypted_key_b64)
        secret_key = base64.b64decode(secret_key_b64)
        nonce = base64.b64decode(nonce_b64)
        tag = base64.b64decode(tag_b64)

        # ✅ Decapsulate the Kyber shared secret
        shared_secret = kyber.decaps(secret_key, encrypted_key)

        # ✅ Use HKDF to derive AES-256 key
        hkdf = HKDF(
            algorithm=hashes.SHA3_512(),  # Stronger post-quantum security
            length=32,  # AES-256 key size
            salt=None,
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
        print(f"❌ Decryption failed: {str(e)}")
        return None


# ✅ User Input Mode
if __name__ == "__main__":
    print("🔑 Provide the required decryption keys:")
    encrypted_filepath = input("Enter path to the encrypted file: ").strip()
    encrypted_key_b64 = input("Enter Base64-encoded encrypted AES key: ").strip()
    secret_key_b64 = input("Enter Base64-encoded Kyber secret key: ").strip()
    nonce_b64 = input("Enter Base64-encoded nonce: ").strip()
    tag_b64 = input("Enter Base64-encoded authentication tag: ").strip()

    decrypted_file = decrypt_file_kyber_aes(
        encrypted_filepath, encrypted_key_b64, secret_key_b64, nonce_b64, tag_b64
    )

    if decrypted_file:
        print(f"🎉 Decryption successful! File saved as: {decrypted_file}")
    else:
        print("❌ Decryption failed! Check your keys and try again.")
