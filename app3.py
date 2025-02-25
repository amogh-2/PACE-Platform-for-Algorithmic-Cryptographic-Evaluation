from flask import Flask, render_template, request, jsonify, send_file
import os
import base64
from flask_cors import CORS
from script.encrypt_aes_cbc import encrypt_file_aes_cbc
from script.decrypt_aes_cbc import decrypt_file_aes_cbc
from script.encrypt_aes_gcm import encrypt_file_aes_gcm
from script.decrypt_aes_gcm import decrypt_file_aes_gcm
from script.encrypt_chacha20 import encrypt_file_chacha20
from script.decrypt_chacha20 import decrypt_file_chacha20
from script.encrypt_chacha20_poly1305 import encrypt_file_chacha20_poly1305
from script.decrypt_chacha20_poly1305 import decrypt_file_chacha20_poly1305
from script.encrypt_kyber_aes import encrypt_file_kyber_aes
from script.decrypt_kyber_aes import decrypt_file_kyber_aes

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "/home/amogh/Downloads/temp/try_api/uploads"
ENCRYPTED_FOLDER = "/home/amogh/Downloads/temp/try_api/encrypted"
DECRYPTED_FOLDER = "/home/amogh/Downloads/temp/try_api/decrypted"

# Create necessary folders
for folder in [UPLOAD_FOLDER, ENCRYPTED_FOLDER, DECRYPTED_FOLDER]:
    os.makedirs(folder, exist_ok=True)

@app.route("/")
def index():
    return render_template("/index.html")

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

@app.route("/kyber_aes_enc_dec")
def kyber_aes_enc_dec():
    return render_template("enc_dec_algorithms/kyber-aes-256.html")

@app.route("/encrypt", methods=["POST"])
def encrypt_file():
    if "file" not in request.files or "algorithm" not in request.form:
        return jsonify({"error": "No file uploaded or algorithm not specified"}), 400

    file = request.files["file"]
    algorithm = request.form["algorithm"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if algorithm not in ['aes-cbc', 'aes-gcm', 'chacha20', 'chacha20-poly1305', 'kyber-aes']:
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
        else:  # kyber-aes
            result = encrypt_file_kyber_aes(f)

    if "error" in result:
        return jsonify(result), 500

    # Save encrypted file to encrypted/
    encrypted_path = os.path.join(ENCRYPTED_FOLDER, file.filename + ".enc")
    with open(encrypted_path, "wb") as f:
        f.write(base64.b64decode(result["encrypted_data"]))

    headers = {
        "Algorithm": algorithm
    }

    if algorithm == 'aes-cbc':
        headers["Key"] = result["key"]
        headers["IV"] = result["iv"]
    elif algorithm == 'aes-gcm':
        headers["Key"] = result["key"]
        headers["Nonce"] = result["nonce"]
        headers["Tag"] = result["tag"]
    elif algorithm in ['chacha20', 'chacha20-poly1305']:
        headers["Key"] = result["key"]
        headers["Nonce"] = result["nonce"]
    else:  # kyber-aes
        headers["EncryptedKey"] = result["encrypted_key"]
        headers["Nonce"] = result["nonce"]
        headers["Tag"] = result["tag"]
        headers["PublicKey"] = result["public_key"]
        headers["SecretKey"] = result["secret_key"]

    return send_file(
        encrypted_path,
        as_attachment=True,
        download_name=file.filename + ".enc",
        mimetype="application/octet-stream"
    ), 200, headers

@app.route("/decrypt", methods=["POST"])
def decrypt_file():
    if "file" not in request.files or "algorithm" not in request.form:
        return jsonify({"error": "Missing file or algorithm"}), 400

    file = request.files["file"]
    algorithm = request.form["algorithm"]

    if algorithm not in ['aes-cbc', 'aes-gcm', 'chacha20', 'chacha20-poly1305', 'kyber-aes']:
        return jsonify({"error": "Unsupported algorithm"}), 400

    # Save encrypted file to encrypted/
    encrypted_path = os.path.join(ENCRYPTED_FOLDER, file.filename)
    file.save(encrypted_path)

    try:
        if algorithm == 'aes-cbc':
            key = request.form["key"]
            iv = request.form["iv"]
            decrypted_path = decrypt_file_aes_cbc(encrypted_path, key, iv)
        elif algorithm == 'aes-gcm':
            key = request.form["key"]
            nonce = request.form["nonce"]
            tag = request.form["tag"]
            decrypted_path = decrypt_file_aes_gcm(encrypted_path, key, nonce, tag)
        elif algorithm == 'chacha20':
            key = request.form["key"]
            nonce = request.form["nonce"]
            decrypted_path = decrypt_file_chacha20(encrypted_path, key, nonce)
        elif algorithm == 'chacha20-poly1305':
            key = request.form["key"]
            nonce = request.form["nonce"]
            decrypted_path = decrypt_file_chacha20_poly1305(encrypted_path, key, nonce)
        else:  # kyber-aes
            encrypted_key = request.form["encrypted_key"]
            secret_key = request.form["secret_key"]
            nonce = request.form["nonce"]
            tag = request.form["tag"]
            decrypted_path = decrypt_file_kyber_aes(encrypted_path, encrypted_key, secret_key, nonce, tag)

        return send_file(
            decrypted_path,
            as_attachment=True,
            download_name=os.path.basename(decrypted_path),
            mimetype="application/octet-stream"
        )
    except Exception as e:
        return jsonify({"error": "Decryption failed", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

