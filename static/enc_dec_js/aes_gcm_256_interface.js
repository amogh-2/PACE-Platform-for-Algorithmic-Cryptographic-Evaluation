document.addEventListener('DOMContentLoaded', () => {
    const encryptFileInput = document.getElementById('encryptFileInput');
    const encryptButton = document.getElementById('encryptButton');
    const encryptionDetails = document.getElementById('encryption-details');
    const downloadLink = document.getElementById('download-link');

    const decryptFileInput = document.getElementById('decryptFileInput');
    const decryptKey = document.getElementById('decryptKey');
    const decryptNonce = document.getElementById('decryptNonce');
    const decryptTag = document.getElementById('decryptTag');
    const decryptButton = document.getElementById('decryptButton');
    const decryptionDetails = document.getElementById('decryption-details');
    const decryptDownloadLink = document.getElementById('decrypt-download-link');

    // Encryption handler
    encryptButton.addEventListener('click', () => {
        const file = encryptFileInput.files[0];
        if (!file) {
            alert('Please select a file to encrypt');
            return;
        }

        console.log('Encrypt button clicked');
        console.log('File selected:', file.name);

        const formData = new FormData();
        formData.append('file', file);
        formData.append('algorithm', 'aes-256-gcm'); // Changed to AES-256-GCM

        fetch('/encrypt', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            console.log('Encryption response status:', response.status);
            if (!response.ok) {
                return response.text().then(errorText => {
                    throw new Error(`Encryption failed: ${errorText}`);
                });
            }
            const key = response.headers.get('Key');
            const nonce = response.headers.get('Nonce');
            const tag = response.headers.get('Tag');
            console.log('Encryption details:', { key, nonce, tag });
            encryptionDetails.textContent = `Key: ${key}\nNonce: ${nonce}\nTag: ${tag}`;
            return response.blob();
        })
        .then(blob => {
            console.log('Encrypted file blob received');
            const url = URL.createObjectURL(blob);
            downloadLink.href = url;
            downloadLink.download = `${file.name}.enc`;
            downloadLink.style.display = 'inline-block';
            downloadLink.textContent = 'Download Encrypted File';
        })
        .catch(error => {
            console.error('Encryption error:', error);
            alert(`Encryption failed: ${error.message}`);
        });
    });

    // Decryption handler
    decryptButton.addEventListener('click', () => {
        const file = decryptFileInput.files[0];
        const key = decryptKey.value;
        const nonce = decryptNonce.value;
        const tag = decryptTag.value;

        console.log('Decrypt button clicked');
        console.log('File:', file ? file.name : 'None');
        console.log('Key:', key);
        console.log('Nonce:', nonce);
        console.log('Tag:', tag);

        if (!file || !key || !nonce || !tag) {
            alert('Please provide a file, key, nonce, and tag for decryption');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        formData.append('key', key);
        formData.append('nonce', nonce);
        formData.append('tag', tag);
        formData.append('algorithm', 'aes-256-gcm'); // Changed to AES-256-GCM

        console.log('Sending decryption request to /decrypt');

        fetch('/decrypt', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            console.log('Decryption response status:', response.status);
            if (!response.ok) {
                return response.text().then(errorText => {
                    throw new Error(`Decryption failed: ${errorText}`);
                });
            }
            return response.blob();
        })
        .then(blob => {
            console.log('Decrypted file blob received');
            const url = URL.createObjectURL(blob);
            decryptDownloadLink.href = url;
            decryptDownloadLink.download = file.name.replace('.enc', '.dec');
            decryptDownloadLink.style.display = 'inline-block';
            decryptDownloadLink.textContent = 'Download Decrypted File';
            decryptionDetails.textContent = 'Decryption successful!';
        })
        .catch(error => {
            console.error('Decryption error:', error);
            alert(`Decryption failed: ${error.message}`);
        });
    });
});