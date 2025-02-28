from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import time
import base64
import platform
import subprocess
import re

def encrypt_file_aes_cbc(file):
    try:
        execution_time = time.perf_counter()
        key = os.urandom(16)  # AES_cbc-128 key (16 bytes)
        iv = os.urandom(16)   # IV (16 bytes)
        
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        file_data = file.read()
        start_time= time.perf_counter()
        padded_data = file_data + b' ' * (16 - len(file_data) % 16)  # PKCS7 padding
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()  # noqa: F841
        encryption_time=  time.perf_counter()-start_time
        global execution_time_enc
        execution_time_enc = time.perf_counter() - execution_time
        return {
               "encryption_time": encryption_time,
                  }
    except Exception as e:
        return {"error": f"Encryption failed: {str(e)}"}


def decrypt_file_aes_cbc(filepath, key_b64, iv_b64):
    try:
        execution_time = time.perf_counter()
        key = base64.b64decode(key_b64)
        iv = base64.b64decode(iv_b64)

        with open(filepath, 'rb') as file:
            encrypted_data = file.read()

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        start_time= time.perf_counter()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        pad_length = decrypted_data[-1]
        decrypted_data = decrypted_data[:-pad_length]
        decryption_time= time.perf_counter()-start_time
        execution_time_dec = time.perf_counter() - execution_time
        execution_time_aes_cbc = execution_time_enc + execution_time_dec
        decrypted_filepath = filepath.replace(".enc", ".dec")
        with open(decrypted_filepath, 'wb') as file:
            file.write(decrypted_data)

        return{
            "decryption_time": decryption_time,
            "execution_time_aes_cbc": execution_time_aes_cbc,
        } 
    except Exception as e:
        raise Exception(f"Decryption failed: {str(e)}")
    
def get_system_info():
    try:
        # Extract raw CPU model name from lscpu
        cpu_model = subprocess.check_output(
            "lscpu | grep 'Model name' | awk -F ':' '{print $2}'", 
            shell=True, text=True
        ).strip()

        # Clean up the model name for consistency
        cpu_model = re.sub(r'\s*\(R\)|\s*\(TM\)|\s*Core|Processor', '', cpu_model)  # Remove (R), (TM), "Core", "Processor"
        cpu_model = re.sub(r'\s+', ' ', cpu_model).strip()  # Normalize spaces
    except Exception as e:
        cpu_model = str(e)
    os_name = platform.system()
    return cpu_model, os_name 