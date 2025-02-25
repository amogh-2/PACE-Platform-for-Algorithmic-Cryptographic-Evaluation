document.addEventListener("DOMContentLoaded", () => {
    const aesCbcButton = document.getElementById("aesCbcButton")
    const aesGcmButton = document.getElementById("aesGcmButton")
    const chacha20Button = document.getElementById("chacha20Button")
    const chacha20Poly1305Button = document.getElementById("chacha20Poly1305Button")
    const kyberAesButton = document.getElementById("kyberAesButton")
  
    aesCbcButton.addEventListener("click", () => {
      window.location.href = "/aes_cbc_enc_dec"
    })
  
    aesGcmButton.addEventListener("click", () => {
      window.location.href = "/aes_gcm_enc_dec"
    })
  
    chacha20Button.addEventListener("click", () => {
      window.location.href = "/chacha20_enc_dec"
    })
  
    chacha20Poly1305Button.addEventListener("click", () => {
      window.location.href = "/chacha20_poly1305_enc_dec"
    })
  
    kyberAesButton.addEventListener("click", () => {
      window.location.href = "/kyber_aes_enc_dec"
    })
  })
  
  