import os
import base64
#import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from kyber_py.kyber.kyber import Kyber  # Import the Kyber class
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

# Initialize Kyber
kyber = Kyber(parameter_set={"k": 2, "eta_1": 3, "eta_2": 2, "du": 10, "dv": 4})

def encrypt_file_kyber_aes(filepath):
    try:
        # ✅ Read the file data
        with open(filepath, "rb") as file:
            file_data = file.read()

        # ✅ Generate Kyber key pair
        public_key, secret_key = kyber.keygen()

        # ✅ Encrypt AES key using Kyber KEM
        shared_secret, encrypted_key = kyber.encaps(public_key)

        # ✅ Use HKDF to derive a secure AES-256 key
        hkdf = HKDF(
            algorithm=hashes.SHA3_512(),  # Stronger post-quantum security
            length=32,  # AES-256 key size
            salt=None,
            info=b"Kyber-AES Encryption",
            backend=default_backend()
        )
        aes_key = hkdf.derive(shared_secret)

        # ✅ AES-GCM encryption
        nonce = os.urandom(12)  # 96-bit nonce
        cipher = Cipher(algorithms.AES(aes_key), modes.GCM(nonce), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(file_data) + encryptor.finalize()

        # ✅ Save encrypted file
        encrypted_filepath = filepath + ".enc"
        with open(encrypted_filepath, "wb") as file:
            file.write(encrypted_data)

        # ✅ Display required decryption values in Base64
        return {
            "encrypted_file": encrypted_filepath,
            "encrypted_key": base64.b64encode(encrypted_key).decode(),
            "public_key": base64.b64encode(public_key).decode(),
            "secret_key": base64.b64encode(secret_key).decode(),  # ⚠️ Store securely!
            "nonce": base64.b64encode(nonce).decode(),
            "tag": base64.b64encode(encryptor.tag).decode(),
        }

    except Exception as e:
        return {"error": f"Encryption failed: {str(e)}"}
