from flask import Flask, render_template, request, jsonify, send_file
import os
import base64
import json
from flask_cors import CORS
from enc_dec_script.encrypt_aes_cbc import encrypt_file_aes_cbc
from enc_dec_script.encrypt_aes_cbc import decrypt_file_aes_cbc
from enc_dec_script.encrypt_aes_gcm import encrypt_file_aes_gcm
from enc_dec_script.encrypt_aes_gcm import decrypt_file_aes_gcm
from enc_dec_script.encrypt_chacha20 import encrypt_file_chacha20
from enc_dec_script.encrypt_chacha20 import decrypt_file_chacha20
from enc_dec_script.encrypt_chacha20_poly1305 import encrypt_file_chacha20_poly1305
from enc_dec_script.encrypt_chacha20_poly1305  import decrypt_file_chacha20_poly1305
from processor_page_script.aes_cbc import run_benchmark

app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app)

UPLOAD_FOLDER = "/home/amogh/Downloads/temp/try_api/uploads"
ENCRYPTED_FOLDER = "/home/amogh/Downloads/temp/try_api/encrypted"
DECRYPTED_FOLDER = "/home/amogh/Downloads/temp/try_api/decrypted"
ENCRYPTION_INFO_FOLDER = "/home/amogh/Downloads/temp/try_api/encryption_info"
BENCHMARK_RESULTS_FOLDER = "/home/amogh/Downloads/temp/try_api/benchmark_results"

# Create necessary folders
for folder in [UPLOAD_FOLDER, ENCRYPTED_FOLDER, DECRYPTED_FOLDER, ENCRYPTION_INFO_FOLDER, BENCHMARK_RESULTS_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# Path to store benchmark results
AES_CBC_RESULTS_FILE = os.path.join(BENCHMARK_RESULTS_FOLDER, "aes_cbc_benchmark_results.json")

@app.route("/")
def index():
    return render_template("/index.html")

@app.route("/processor_choosing")
def processor_choosing():
    return render_template("/processor_benchmarking/processor_choose.html")

@app.route("/aes_cbc_128_pro")
def aes_cbc_128_pro():
    return render_template("/processor_benchmarking/processor_particular/aes-cbc-128-pro.html")

@app.route("/aes_gcm_128_pro")
def aes_gcm_128_pro():
    return render_template("/processor_benchmarking/processor_particular/aes-gcm-128-pro.html")

@app.route("/chacha20_poly1305_pro")
def chacha20_poly1305_pro():
    return render_template("/processor_benchmarking/processor_particular/chacha20-poly1305-pro.html")

@app.route("/chacha20_pro")
def chacha20_pro():
    return render_template("/processor_benchmarking/processor_particular/chacha20pro.html")

@app.route("/kyber_aes_pro")
def kyber_aes_pro():
    return render_template("/processor_benchmarking/processor_particular/kyber-aes-256-pro.html")

@app.route("/kyber_chacha20_poly1305_pro")
def kyber_chacha20_poly1305_pro():
    return render_template("/processor_benchmarking/processor_particular/kyber-chacha20-poly-pro.html")

@app.route("/aes_cbc_enc_dec")
def aes_cbc_enc_dec():
    return render_template("enc_dec_algorithms/aes-cbc-128.html")

@app.route("/aes_gcm_enc_dec")
def aes_gcm_enc_dec():
    return render_template("enc_dec_algorithms/aes-gcm-128.html")

@app.route("/chacha20_enc_dec")
def chacha20_enc_dec():
    return render_template("enc_dec_algorithms/chacha20.html")

@app.route("/chacha20_poly1305_enc_dec")
def chacha20_poly1305_enc_dec():
    return render_template("enc_dec_algorithms/chacha20-poly1305.html")

@app.route("/download_encrypted/<filename>")
def download_encrypted(filename):
    return send_file(os.path.join(ENCRYPTED_FOLDER, filename), as_attachment=True)

@app.route("/download_info/<filename>")
def download_info(filename):
    return send_file(os.path.join(ENCRYPTION_INFO_FOLDER, filename), as_attachment=True)

@app.route("/encrypt", methods=["POST"])
def encrypt_file():
    if "file" not in request.files or "algorithm" not in request.form:
        return jsonify({"error": "No file uploaded or algorithm not specified"}), 400

    file = request.files["file"]
    algorithm = request.form["algorithm"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if algorithm not in ['aes-cbc', 'aes-gcm', 'chacha20', 'chacha20-poly1305']:
        return jsonify({"error": "Unsupported algorithm"}), 400

    # Save original file to uploads/
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # Encrypt the file
    with open(file_path, "rb") as f:
        if algorithm == 'aes-cbc':
            result = encrypt_file_aes_cbc(f)
        elif algorithm == 'aes-gcm':
            result = encrypt_file_aes_gcm(f)
        elif algorithm == 'chacha20':
            result = encrypt_file_chacha20(f)
        elif algorithm == 'chacha20-poly1305':
            result = encrypt_file_chacha20_poly1305(f)

    if "error" in result:
        return jsonify(result), 500

    # Save encrypted file to encrypted/
    encrypted_path = os.path.join(ENCRYPTED_FOLDER, file.filename + ".enc")
    with open(encrypted_path, "wb") as f:
        f.write(base64.b64decode(result["encrypted_data"]))

    # Create response with encrypted file
    response = send_file(
        encrypted_path,
        as_attachment=True,
        download_name=file.filename + ".enc",
        mimetype="application/octet-stream"
    )
    
    # Add encryption parameters to response headers
    if "key" in result:
        response.headers["Key"] = result["key"]
    if "iv" in result:
        response.headers["IV"] = result["iv"]
    if "nonce" in result:
        response.headers["Nonce"] = result["nonce"]
    if "tag" in result:
        response.headers["Tag"] = result["tag"]
        
    return response

@app.route("/decrypt", methods=["POST"])
def decrypt_file():
    if "file" not in request.files or "algorithm" not in request.form:
        return jsonify({"error": "Missing file or algorithm"}), 400

    file = request.files["file"]
    algorithm = request.form["algorithm"]

    if algorithm not in ['aes-cbc', 'aes-gcm', 'chacha20', 'chacha20-poly1305']:
        return jsonify({"error": "Unsupported algorithm"}), 400

    # Save encrypted file to encrypted/
    encrypted_path = os.path.join(ENCRYPTED_FOLDER, file.filename)
    file.save(encrypted_path)
    
    try:
        # Process based on algorithm
        if algorithm == 'aes-cbc':
            key = request.form.get('key')
            iv = request.form.get('iv')
            if not key or not iv:
                return jsonify({"error": "Key and IV are required for AES-CBC decryption"}), 400
            decrypted_path = decrypt_file_aes_cbc(encrypted_path, key, iv)
            
        elif algorithm == 'aes-gcm':
            key = request.form.get('key')
            nonce = request.form.get('nonce')
            tag = request.form.get('tag')
            if not key or not nonce or not tag:
                return jsonify({"error": "Key, nonce, and tag are required for AES-GCM decryption"}), 400
            decrypted_path = decrypt_file_aes_gcm(encrypted_path, key, nonce, tag)
            
        elif algorithm == 'chacha20':
            key = request.form.get('key')
            nonce = request.form.get('nonce')
            if not key or not nonce:
                return jsonify({"error": "Key and nonce are required for ChaCha20 decryption"}), 400
            decrypted_path = decrypt_file_chacha20(encrypted_path, key, nonce)
            
        elif algorithm == 'chacha20-poly1305':
            key = request.form.get('key')
            nonce = request.form.get('nonce')
            if not key or not nonce:
                return jsonify({"error": "Key and nonce are required for ChaCha20-Poly1305 decryption"}), 400
            decrypted_path = decrypt_file_chacha20_poly1305(encrypted_path, key, nonce)

        # If we get here, decryption was successful
        return send_file(
            decrypted_path,
            as_attachment=True,
            download_name=os.path.basename(decrypted_path),
            mimetype="application/octet-stream"
        )
    except Exception as e:
        return jsonify({"error": f"Decryption failed: {str(e)}"}), 400



# Processor benchmarking routes and functions
@app.route("/run_aes_cbc_benchmark", methods=["POST"])
def aes_cbc_benchmark():
    try:
        data = request.json
        file_size = data.get("fileSize", "5MB")
        
        # Run the benchmark
        result = run_benchmark(file_size)
        
        if "error" in result:
            return jsonify({"error": result["error"]}), 500
        
        # Save result to file
        save_benchmark_result(result)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_aes_cbc_benchmark_results", methods=["GET"])
def get_benchmark_results():
    try:
        results = load_benchmark_results()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def save_benchmark_result(result):
    """Save benchmark result to a JSON file"""
    try:
        # Load existing results
        results = load_benchmark_results()
        
        # Add new result
        results.append(result)
        
        # Save all results back to file
        with open(AES_CBC_RESULTS_FILE, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Benchmark result saved to {AES_CBC_RESULTS_FILE}")
    except Exception as e:
        print(f"Error saving benchmark result: {e}")

def load_benchmark_results():
    """Load benchmark results from the JSON file"""
    if not os.path.exists(AES_CBC_RESULTS_FILE):
        return []
    
    try:
        with open(AES_CBC_RESULTS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading benchmark results: {e}")
        return []

if __name__ == "__main__":
    app.run(debug=True)

