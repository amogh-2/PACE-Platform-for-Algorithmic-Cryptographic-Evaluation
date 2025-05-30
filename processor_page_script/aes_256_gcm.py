from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import time
import base64
import platform
import subprocess
import re
from datetime import datetime

def encrypt_file_aes_gcm(file_path):
    try:
        execution_time = time.perf_counter()
        key = os.urandom(32)  # AES-256 key (32 bytes)
        nonce = os.urandom(12)  # GCM typically uses 12 bytes for nonce
        
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
        encryptor = cipher.encryptor()

        with open(file_path, 'rb') as file:
            file_data = file.read()
            
        start_time = time.perf_counter()
        encrypted_data = encryptor.update(file_data) + encryptor.finalize()
        auth_tag = encryptor.tag
        encryption_time = time.perf_counter() - start_time
        
        encrypted_file_path = file_path + ".enc"
        with open(encrypted_file_path, 'wb') as file:
            file.write(encrypted_data + auth_tag)
            
        execution_time_enc = time.perf_counter() - execution_time
        
        return {
            "encryption_time": encryption_time,
            "execution_time_enc": execution_time_enc,
            "key": base64.b64encode(key).decode('utf-8'),
            "nonce": base64.b64encode(nonce).decode('utf-8'),
            "encrypted_file_path": encrypted_file_path
        }
    except Exception as e:
        return {"error": f"Encryption failed: {str(e)}"}

def decrypt_file_aes_gcm(filepath, key_b64, nonce_b64):
    try:
        execution_time = time.perf_counter()
        key = base64.b64decode(key_b64)
        nonce = base64.b64decode(nonce_b64)

        with open(filepath, 'rb') as file:
            data = file.read()
        
        auth_tag = data[-16:]
        encrypted_data = data[:-16]

        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, auth_tag), backend=default_backend())
        decryptor = cipher.decryptor()
        
        start_time = time.perf_counter()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        decryption_time = time.perf_counter() - start_time
        execution_time_dec = time.perf_counter() - execution_time
        
        os.remove(filepath)
        
        return {
            "decryption_time": decryption_time,
            "execution_time_dec": execution_time_dec
        }
    except Exception as e:
        return {"error": f"Decryption failed: {str(e)}"}

def get_system_info():
    try:
        cpu_model = subprocess.check_output(
            "lscpu | grep 'Model name' | awk -F ':' '{print $2}'", 
            shell=True, text=True
        ).strip()
        cpu_model = re.sub(r'\s*$$R$$|\s*$$TM$$|\s*Core|Processor', '', cpu_model)
        cpu_model = re.sub(r'\s+', ' ', cpu_model).strip()
    except Exception as e:
        cpu_model = platform.processor()
    
    os_name = platform.system()
    return cpu_model, os_name

def create_test_file(size_mb):
    size_bytes = size_mb * 1024 * 1024
    test_file_path = f"test_data/{size_mb}MB.txt"
    os.makedirs("test_data", exist_ok=True)
    with open(test_file_path, 'wb') as f:
        f.write(os.urandom(size_bytes))
    return test_file_path

def save_benchmark_result(result, benchmark_folder):
    os.makedirs(benchmark_folder, exist_ok=True)
    filename = f"aes_256_gcm_{result['file_size']}.txt"
    filepath = os.path.join(benchmark_folder, filename)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result_line = f"{timestamp},{result['cpu_model']},{result['os_name']},{result['file_size']},{result['encryption_time']},{result['decryption_time']},{result['execution_time']}\n"
    
    with open(filepath, 'a') as f:
        f.write(result_line)
    return filepath

def run_aes_256_gcm_benchmark(file_size, benchmark_folder="benchmark_results"):
    try:
        size_mb = int(file_size.replace("MB", ""))
        file_path = create_test_file(size_mb)
        cpu_model, os_name = get_system_info()
        
        encryption_result = encrypt_file_aes_gcm(file_path)
        if "error" in encryption_result:
            return {"error": encryption_result["error"]}
        
        decryption_result = decrypt_file_aes_gcm(
            encryption_result["encrypted_file_path"],
            encryption_result["key"],
            encryption_result["nonce"]
        )
        
        if "error" in decryption_result:
            return {"error": decryption_result["error"]}
        
        execution_time = encryption_result["execution_time_enc"] + decryption_result["execution_time_dec"]
        
        try:
            os.remove(file_path)
        except:
            pass
        
        result = {
            "cpu_model": cpu_model,
            "os_name": os_name,
            "file_size": file_size,
            "encryption_time": round(encryption_result["encryption_time"], 3),
            "decryption_time": round(decryption_result["decryption_time"], 3),
            "execution_time": round(execution_time, 3)
        }
        
        save_benchmark_result(result, benchmark_folder)
        return result
    except Exception as e:
        return {"error": str(e)}