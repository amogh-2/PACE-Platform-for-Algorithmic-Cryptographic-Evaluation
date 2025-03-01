document.addEventListener("DOMContentLoaded", () => {
    const aes128cbc= document.getElementById("aes128cbc")
    const aes128gcm = document.getElementById("aes128gcm")
    const chacha20 = document.getElementById("chacha20")
    const chacha20poly1305= document.getElementById("chacha20poly1305")
    const aes256cbcButton = document.getElementById("aes256cbc")
    const aes256gcmButton = document.getElementById("aes256gcm")
    
    aes128cbc.addEventListener("click", () => {
      window.location.href = "/aes_cbc_128_pro"
    })
  
    aes128gcm.addEventListener("click", () => {
      window.location.href = "/aes_gcm_128_pro"
    })
  
    chacha20.addEventListener("click", () => {
      window.location.href = "/chacha20_pro"
    })
  
    chacha20poly1305.addEventListener("click", () => {
      window.location.href = "/chacha20_poly1305_pro"
    })
  
    aes256cbcButton.addEventListener("click", () => {
      window.location.href = "/aes_256_cbc_pro"
    })
  
    aes256gcmButton.addEventListener("click", () => {
      window.location.href = "/aes_256_gcm_pro"
    })
  
  })
  
  