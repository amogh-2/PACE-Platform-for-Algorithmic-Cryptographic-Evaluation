document.addEventListener("DOMContentLoaded", () => {
  const encryptFileInput = document.getElementById("encryptFileInput")
  const encryptButton = document.getElementById("encryptButton")
  const encryptionDetails = document.getElementById("encryption-details")
  const downloadLink = document.getElementById("download-link")

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
      .then((response) => {
        if (!response.ok) {
          throw new Error("Encryption failed")
        }
        const encryptedKey = response.headers.get("EncryptedKey")
        const nonce = response.headers.get("Nonce")
        const tag = response.headers.get("Tag")
        const publicKey = response.headers.get("PublicKey")
        const secretKey = response.headers.get("SecretKey")
        encryptionDetails.textContent = `Encrypted Key: ${encryptedKey}\nNonce: ${nonce}\nTag: ${tag}\nPublic Key: ${publicKey}\nSecret Key: ${secretKey}`
        return response.blob()
      })
      .then((blob) => {
        const url = URL.createObjectURL(blob)
        downloadLink.href = url
        downloadLink.download = `${file.name}.enc`
        downloadLink.style.display = "inline-block"
        downloadLink.textContent = "Download Encrypted File"
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

