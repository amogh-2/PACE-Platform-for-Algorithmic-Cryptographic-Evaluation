from flask import Flask, render_template, request, jsonify, send_file
import os
import base64
from flask_cors import CORS
from script.encrypt_aes_cbc import encrypt_file_aes_cbc
from script.decrypt_aes_cbc import decrypt_file_aes_cbc
from script.encrypt_chacha20 import encrypt_file_chacha20 
from script.decrypt_chacha20 import decrypt_file_chacha20 
from script.encrypt_aes_gcm import encrypt_file_aes_gcm
from script.decrypt_aes_gcm import decrypt_file_aes_gcm

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
def aes_enc_dec():
    return render_template("enc_dec_algorithms/aes_cbc-128.html")

@app.route("/aes_gcm_enc_dec")
def aes_gcm_enc_dec():
    return render_template("enc_dec_algorithms/aes_gcm-128.html")

@app.route("/chacha20_enc_dec")
def chacha20_enc_dec():
    return render_template("enc_dec_algorithms/chacha20.html")

@app.route("/encrypt", methods=["POST"])
def encrypt_file():
    if "file" not in request.files or "algorithm" not in request.form:
        return jsonify({"error": "No file uploaded or algorithm not specified"}), 400

    file = request.files["file"]
    algorithm = request.form["algorithm"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if algorithm not in ['aes_cbc', 'aes-gcm', 'chacha20']:
        return jsonify({"error": "Unsupported algorithm"}), 400

    # Save original file to uploads/
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # Encrypt the file
    with open(file_path, "rb") as f:
        if algorithm == 'aes_cbc':
            result = encrypt_file_aes_cbc(f)
        elif algorithm == 'aes-gcm':
            result = encrypt_file_aes_gcm(f)
        else:  # chacha20
            result = encrypt_file_chacha20(f)

    if "error" in result:
        return jsonify(result), 500

    # Save encrypted file to encrypted/
    encrypted_path = os.path.join(ENCRYPTED_FOLDER, file.filename + ".enc")
    with open(encrypted_path, "wb") as f:
        f.write(base64.b64decode(result["encrypted_data"]))

    headers = {
        "Key": result["key"],
        "Algorithm": algorithm
    }

    if algorithm == 'aes_cbc':
        headers["IV_or_Nonce"] = result["iv"]
    elif algorithm == 'aes-gcm':
        headers["Nonce"] = result["nonce"]
        headers["Tag"] = result["tag"]
    else:  # chacha20
        headers["IV_or_Nonce"] = result["nonce"]

    return send_file(
        encrypted_path,
        as_attachment=True,
        download_name=file.filename + ".enc",
        mimetype="application/octet-stream"
    ), 200, headers

@app.route("/decrypt", methods=["POST"])
def decrypt_file():
    if "file" not in request.files or "key" not in request.form or "algorithm" not in request.form:
        return jsonify({"error": "Missing file, key, or algorithm"}), 400

    file = request.files["file"]
    key = request.form["key"]
    algorithm = request.form["algorithm"]

    if algorithm not in ['aes_cbc', 'aes-gcm', 'chacha20']:
        return jsonify({"error": "Unsupported algorithm"}), 400

    # Save encrypted file to encrypted/
    encrypted_path = os.path.join(ENCRYPTED_FOLDER, file.filename)
    file.save(encrypted_path)

    try:
        if algorithm == 'aes_cbc':
            iv_or_nonce = request.form["iv_or_nonce"]
            decrypted_path = decrypt_file_aes_cbc(encrypted_path, key, iv_or_nonce)
        elif algorithm == 'aes-gcm':
            nonce = request.form["nonce"]
            tag = request.form["tag"]
            decrypted_path = decrypt_file_aes_gcm(encrypted_path, key, nonce, tag)
        else:  # chacha20
            iv_or_nonce = request.form["iv_or_nonce"]
            decrypted_path = decrypt_file_chacha20(encrypted_path, key, iv_or_nonce)

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