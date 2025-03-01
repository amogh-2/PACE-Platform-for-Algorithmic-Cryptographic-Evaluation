// Updating AES-CBC JavaScript (aes_cbc_interface.js)
document.addEventListener("DOMContentLoaded", () => {
  const encryptFileInput = document.getElementById("encryptFileInput");
  const encryptButton = document.getElementById("encryptButton");
  const encryptionDetails = document.getElementById("encryption-details");
  const downloadLink = document.getElementById("download-link");
  const decryptFileInput = document.getElementById("decryptFileInput");
  const decryptKey = document.getElementById("decryptKey");
  const decryptIV = document.getElementById("decryptIV");
  const decryptButton = document.getElementById("decryptButton");
  const decryptionDetails = document.getElementById("decryption-details");
  const decryptDownloadLink = document.getElementById("decrypt-download-link");

  encryptButton.addEventListener("click", () => {
    const file = encryptFileInput.files[0];
    if (!file) {
      alert("Please select a file to encrypt");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("algorithm", "aes-cbc");

    fetch("/encrypt", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) throw new Error(data.error);
        encryptionDetails.innerHTML = `<p><strong>Key:</strong> ${data.key}</p><p><strong>IV:</strong> ${data.iv}</p>`;
        downloadLink.href = data.encrypted_file;
        downloadLink.style.display = "inline-block";
      })
      .catch((error) => {
        encryptionDetails.innerHTML = `<p class='error'>Encryption failed: ${error.message}</p>`;
      });
  });

  decryptButton.addEventListener("click", () => {
    const file = decryptFileInput.files[0];
    const key = decryptKey.value;
    const iv = decryptIV.value;
    if (!file || !key || !iv) {
      alert("Please provide a file, key, and IV");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("key", key);
    formData.append("iv", iv);
    formData.append("algorithm", "aes-cbc");

    fetch("/decrypt", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.blob())
      .then((blob) => {
        const url = URL.createObjectURL(blob);
        decryptDownloadLink.href = url;
        decryptDownloadLink.download = file.name.replace(".enc", "");
        decryptDownloadLink.style.display = "inline-block";
        decryptionDetails.textContent = "Decryption successful!";
      })
      .catch((error) => {
        decryptionDetails.innerHTML = `<p class='error'>Decryption failed: ${error.message}</p>`;
      });
  });
});