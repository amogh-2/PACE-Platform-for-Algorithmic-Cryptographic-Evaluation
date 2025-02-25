import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from kyber_py.kyber.kyber import Kyber
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

kyber = Kyber(parameter_set={"k": 2, "eta_1": 3, "eta_2": 2, "du": 10, "dv": 4})

def decrypt_file_kyber_aes(filepath, encrypted_key_b64, secret_key_b64, nonce_b64, tag_b64):
    try:
        # Decode Base64 inputs
        encrypted_key = base64.b64decode(encrypted_key_b64)
        secret_key = base64.b64decode(secret_key_b64)
        nonce = base64.b64decode(nonce_b64)
        tag = base64.b64decode(tag_b64)

        # Decrypt shared secret using Kyber KEM
        shared_secret = kyber.decaps(secret_key, encrypted_key)

        # Use HKDF to derive the AES-256 key from the shared secret
        hkdf = HKDF(
            algorithm=hashes.SHA3_512(),
            length=32,
            salt=None,
            info=b"Kyber-AES Encryption",
            backend=default_backend()
        )
        aes_key = hkdf.derive(shared_secret)

        # Read encrypted file data
        with open(filepath, 'rb') as file:
            encrypted_data = file.read()

        # AES-GCM decryption
        cipher = Cipher(algorithms.AES(aes_key), modes.GCM(nonce, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        # Save the decrypted file
        decrypted_filepath = filepath.replace(".enc", ".dec")
        with open(decrypted_filepath, 'wb') as file:
            file.write(decrypted_data)

        return decrypted_filepath

    except Exception as e:
        raise Exception(f"Decryption failed: {str(e)}")