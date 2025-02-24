document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('fileInput');
    const encryptButton = document.getElementById('encryptButton');
    const encryptionDetails = document.getElementById('encryption-details');
    const downloadLink = document.getElementById('download-link');
  
    const decryptFileInput = document.getElementById('decryptFileInput');
    const decryptKey = document.getElementById('decryptKey');
    const decryptIV = document.getElementById('decryptIV');
    const decryptButton = document.getElementById('decryptButton');
    const decryptDownloadLink = document.getElementById('decrypt-download-link');
  
    encryptButton.addEventListener('click', () => {
      const file = fileInput.files[0];
      if (!file) {
        alert('Please select a file to encrypt');
        return;
      }
  
      const formData = new FormData();
      formData.append('file', file);

      fetch('/encrypt', {
        method: 'POST',
        body: formData
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Encryption failed');
        }
        
        const key = response.headers.get('Key');
        const iv = response.headers.get('IV');
        
        encryptionDetails.textContent = `Key: ${key}\nIV: ${iv}`;
        
        return response.blob();
      })
      .then(blob => {
        const url = URL.createObjectURL(blob);
        downloadLink.href = url;
        downloadLink.download = `${file.name}.enc`;
        downloadLink.textContent = 'Download Encrypted File';
        downloadLink.style.display = 'block';
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Encryption failed. Please try again.');
      });
    });
  
    decryptButton.addEventListener('click', () => {
      const file = decryptFileInput.files[0];
      const key = decryptKey.value;
      const iv = decryptIV.value;
  
      if (!file || !key || !iv) {
        alert('Please provide a file, key, and IV for decryption');
        return;
      }
  
      const formData = new FormData();
      formData.append('file', file);
      formData.append('key', key);
      formData.append('iv', iv);
  
      fetch('/decrypt', {
        method: 'POST',
        body: formData
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Decryption failed');
        }
        return response.blob();
      })
      .then(blob => {
        const url = URL.createObjectURL(blob);
        const originalFileName = file.name.replace('.enc', '');
        const fileNameParts = originalFileName.split('.');
        let decryptedFileName;
        if (fileNameParts.length > 1) {
          const extension = fileNameParts.pop();
          decryptedFileName = `${fileNameParts.join('.')}.dec.${extension}`;
        } else {
          decryptedFileName = `${originalFileName}.dec`;
        }
        decryptDownloadLink.href = url;
        decryptDownloadLink.download = decryptedFileName;
        decryptDownloadLink.textContent = 'Download Decrypted File';
        decryptDownloadLink.style.display = 'block';
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Decryption failed. Please check your key and IV.');
      });
    });
  });