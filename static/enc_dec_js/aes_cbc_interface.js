document.addEventListener("DOMContentLoaded", () => {
    const encryptFileInput = document.getElementById("encryptFileInput")
    const encryptButton = document.getElementById("encryptButton")
    const encryptionDetails = document.getElementById("encryption-details")
    const downloadLink = document.getElementById("download-link")
  
    const decryptFileInput = document.getElementById("decryptFileInput")
    const decryptKey = document.getElementById("decryptKey")
    const decryptIV = document.getElementById("decryptIV")
    const decryptButton = document.getElementById("decryptButton")
    const decryptionDetails = document.getElementById("decryption-details")
    const decryptDownloadLink = document.getElementById("decrypt-download-link")
  
    encryptButton.addEventListener("click", () => {
      const file = encryptFileInput.files[0]
      if (!file) {
        alert("Please select a file to encrypt")
        return
      }
  
      const formData = new FormData()
      formData.append("file", file)
      formData.append("algorithm", "aes-cbc")
  
      fetch("/encrypt", {
        method: "POST",
        body: formData,
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Encryption failed")
          }
          return response.json()
        })
        .then((data) => {
          // Display encryption details directly from the response
          encryptionDetails.innerHTML = `
              <p><strong>Key:</strong> ${data.key}</p>
              <p><strong>IV:</strong> ${data.iv}</p>
              <p>Save these values for decryption!</p>
          `
  
          // Set up download link
          downloadLink.href = data.encrypted_file
          downloadLink.style.display = "inline-block"
          downloadLink.textContent = "Download Encrypted File"
  
          // Auto-fill decryption fields for convenience
          decryptKey.value = data.key
          decryptIV.value = data.iv
        })
        .catch((error) => {
          console.error("Error:", error)
          alert("Encryption failed. Please try again.")
        })
    })
  
    decryptButton.addEventListener("click", () => {
      const file = decryptFileInput.files[0]
      const key = decryptKey.value
      const iv = decryptIV.value
  
      if (!file || !key || !iv) {
        alert("Please provide a file, key, and IV for decryption")
        return
      }
  
      const formData = new FormData()
      formData.append("file", file)
      formData.append("key", key)
      formData.append("iv", iv)
      formData.append("algorithm", "aes-cbc")
  
      fetch("/decrypt", {
        method: "POST",
        body: formData,
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Decryption failed")
          }
          return response.blob()
        })
        .then((blob) => {
          const url = URL.createObjectURL(blob)
          decryptDownloadLink.href = url
          decryptDownloadLink.download = file.name.replace(".enc", ".dec")
          decryptDownloadLink.style.display = "inline-block"
          decryptDownloadLink.textContent = "Download Decrypted File"
          decryptionDetails.textContent = "Decryption successful!"
        })
        .catch((error) => {
          console.error("Error:", error)
          alert("Decryption failed. Please check your key and IV.")
        })
    })
  })
  
  