document.addEventListener("DOMContentLoaded", () => {
  const encryptFileInput = document.getElementById("encryptFileInput")
  const encryptButton = document.getElementById("encryptButton")
  const encryptionDetails = document.getElementById("encryption-details")
  const downloadEncryptedLink = document.getElementById("download-encrypted-link")
  const downloadInfoLink = document.getElementById("download-info-link")

  const decryptFileInput = document.getElementById("decryptFileInput")
  const decryptEncryptedKey = document.getElementById("decryptEncryptedKey")
  const decryptSecretKey = document.getElementById("decryptSecretKey")
  const decryptNonce = document.getElementById("decryptNonce")
  const decryptTag = document.getElementById("decryptTag")
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
    formData.append("algorithm", "kyber-aes")

    fetch("/encrypt", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          throw new Error(data.error)
        }
        encryptionDetails.textContent = "Encryption successful!"
        downloadEncryptedLink.href = data.encrypted_file
        downloadEncryptedLink.style.display = "inline-block"
        downloadEncryptedLink.textContent = "Download Encrypted File"
        downloadInfoLink.href = data.encryption_info
        downloadInfoLink.style.display = "inline-block"
        downloadInfoLink.textContent = "Download Encryption Info"
      })
      .catch((error) => {
        console.error("Error:", error)
        alert("Encryption failed. Please try again.")
      })
  })

  decryptButton.addEventListener("click", () => {
    const file = decryptFileInput.files[0]
    const encryptedKey = decryptEncryptedKey.value
    const secretKey = decryptSecretKey.value
    const nonce = decryptNonce.value
    const tag = decryptTag.value

    if (!file || !encryptedKey || !secretKey || !nonce || !tag) {
      alert("Please provide all required information for decryption")
      return
    }

    const formData = new FormData()
    formData.append("file", file)
    formData.append("encrypted_key", encryptedKey)
    formData.append("secret_key", secretKey)
    formData.append("nonce", nonce)
    formData.append("tag", tag)
    formData.append("algorithm", "kyber-aes")

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
        alert("Decryption failed. Please check your input values.")
      })
  })
})