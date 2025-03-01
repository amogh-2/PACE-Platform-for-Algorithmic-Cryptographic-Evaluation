# encrypt_chacha20_kyber.py
import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from kyber_py.kyber.kyber import Kyber
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

kyber = Kyber(parameter_set={"k": 2, "eta_1": 3, "eta_2": 2, "du": 10, "dv": 4})

def encrypt_file_kyber_chacha20(file):
    try:
        public_key, secret_key = kyber.keygen()
        shared_secret, encrypted_key = kyber.encaps(public_key)
        
        hkdf = HKDF(
            algorithm=hashes.SHA3_512(),
            length=32,
            salt=None,
            info=b"Kyber-ChaCha20 Encryption",
            backend=default_backend()
        )
        chacha_key = hkdf.derive(shared_secret)
        
        nonce = os.urandom(16)
        cipher = Cipher(algorithms.ChaCha20(chacha_key, nonce), mode=None, backend=default_backend())
        encryptor = cipher.encryptor()
        
        file_data = file.read()
        encrypted_data = encryptor.update(file_data) + encryptor.finalize()
        
        encryption_info = {
            "encrypted_key": base64.b64encode(encrypted_key).decode(),
            "nonce": base64.b64encode(nonce).decode(),
            "public_key": base64.b64encode(public_key).decode(),
            "secret_key": base64.b64encode(secret_key).decode(),
        }
        
        return {"encrypted_data": base64.b64encode(encrypted_data).decode()}, encryption_info
    except Exception as e:
        return {"error": f"Encryption failed: {str(e)}"}, None