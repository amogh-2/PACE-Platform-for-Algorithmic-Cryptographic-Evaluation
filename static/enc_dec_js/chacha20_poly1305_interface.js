document.addEventListener('DOMContentLoaded', () => {
    const encryptFileInput = document.getElementById('encryptFileInput');
    const encryptButton = document.getElementById('encryptButton');
    const encryptionDetails = document.getElementById('encryption-details');
    const downloadLink = document.getElementById('download-link');

    const decryptFileInput = document.getElementById('decryptFileInput');
    const decryptKey = document.getElementById('decryptKey');
    const decryptNonce = document.getElementById('decryptNonce');
    const decryptButton = document.getElementById('decryptButton');
    const decryptionDetails = document.getElementById('decryption-details');
    const decryptDownloadLink = document.getElementById('decrypt-download-link');

    encryptButton.addEventListener('click', () => {
        const file = encryptFileInput.files[0];
        if (!file) {
            alert('Please select a file to encrypt');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        formData.append('algorithm', 'chacha20-poly1305');

        fetch('/encrypt', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || 'Encryption failed');
                });
            }
            return response.json();
        })
        .then(data => {
            encryptionDetails.innerHTML = `
                <p><strong>Key:</strong> ${data.key}</p>
                <p><strong>Nonce:</strong> ${data.nonce}</p>
                <p>Save these values for decryption!</p>
            `;
            downloadLink.href = data.encrypted_file;
            downloadLink.download = `${file.name}.enc`;
            downloadLink.style.display = 'inline-block';
            downloadLink.textContent = 'Download Encrypted File';

            // Auto-fill decryption fields
            decryptKey.value = data.key;
            decryptNonce.value = data.nonce;
        })
        .catch(error => {
            console.error('Error:', error);
            encryptionDetails.innerHTML = `<p class="error">Encryption failed: ${error.message}</p>`;
        });
    });

    decryptButton.addEventListener('click', () => {
        const file = decryptFileInput.files[0];
        const key = decryptKey.value;
const nonce = decryptNonce.value;

        if (!file || !key || !nonce) {
            alert('Please provide a file, key, and nonce for decryption');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        formData.append('key', key);
        formData.append('nonce', nonce);
        formData.append('algorithm', 'chacha20-poly1305');

        decryptionDetails.textContent = 'Decrypting...';
        decryptDownloadLink.style.display = 'none';

        fetch('/decrypt', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || 'Decryption failed');
                });
            }
            return response.blob();
        })
        .then(blob => {
            const url = URL.createObjectURL(blob);
            decryptDownloadLink.href = url;
            decryptDownloadLink.download = file.name.replace('.enc', '.dec');
            decryptDownloadLink.style.display = 'inline-block';
            decryptDownloadLink.textContent = 'Download Decrypted File';
            decryptionDetails.textContent = 'Decryption successful!';
        })
        .catch(error => {
            console.error('Error:', error);
            decryptionDetails.innerHTML = `<p class="error">Decryption failed: ${error.message}</p>`;
            decryptDownloadLink.style.display = 'none';
        });
    });
});

