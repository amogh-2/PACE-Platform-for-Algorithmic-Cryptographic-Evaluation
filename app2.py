from flask import Flask, render_template, request, jsonify, send_file
import os
import base64
from script.encrypt_aes import encrypt_file_aes
from script.decrypt_aes import decrypt_file_aes

app = Flask(__name__)

UPLOAD_FOLDER = "/home/amogh/Downloads/temp/try_api/uploads"
ENCRYPTED_FOLDER = "/home/amogh/Downloads/temp/try_api/encrypted"
DECRYPTED_FOLDER = "/home/amogh/Downloads/temp/try_api/decrypted"

# Create necessary folders
for folder in [UPLOAD_FOLDER, ENCRYPTED_FOLDER, DECRYPTED_FOLDER]:
    os.makedirs(folder, exist_ok=True)

@app.route("/aes_enc_dec")
def aes_enc_dec():
    return render_template("enc_dec_algorithms/aes-128.html")

@app.route("/encrypt", methods=["POST"])
def encrypt_file_route():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save original file to uploads/
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Encrypt the file
    with open(file_path, "rb") as f:
        result = encrypt_file_aes(f) ##### here it is

    if "error" in result:
        return jsonify(result), 500

    # Save encrypted file to encrypted/
    encrypted_path = os.path.join(ENCRYPTED_FOLDER, file.filename + ".enc")
    with open(encrypted_path, "wb") as f:
        f.write(base64.b64decode(result["encrypted_data"]))

    return send_file(
        encrypted_path,
        as_attachment=True,
        download_name=file.filename + ".enc",
        mimetype="application/octet-stream"
    ), 200, {
        "Key": result["key"],
        "IV": result["iv"]
    }

@app.route("/decrypt", methods=["POST"])
def decrypt_file_route():
    if "file" not in request.files or "key" not in request.form or "iv" not in request.form:
        return jsonify({"error": "Missing file, key, or IV"}), 400

    file = request.files["file"]
    key = request.form["key"]
    iv = request.form["iv"]

    # Save encrypted file to encrypted/
    encrypted_path = os.path.join(ENCRYPTED_FOLDER, file.filename)
    file.save(encrypted_path)

    try:
        # Decrypt the file
        decrypted_path = decrypt_file_aes(encrypted_path, key, iv)  ##### for aes

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