document.addEventListener("DOMContentLoaded", () => {
    const aes128cbc= document.getElementById("aes128cbc")
    const aes128gcm = document.getElementById("aes128gcm")
    const chacha20 = document.getElementById("chacha20")
    const chacha20poly1305= document.getElementById("chacha20poly1305")
    const kyberaes = document.getElementById("kyberaes")
    const kyberchacha20poly = document.getElementById("kyberchacha20poly")
    
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
  
    kyberaes.addEventListener("click", () => {
      window.location.href = "/kyber_aes_pro"
    })
  
    kyberchacha20poly.addEventListener("click", () => {
      window.location.href = "/kyber_chacha20_poly1305_pro"
    })
  
  })
  
  