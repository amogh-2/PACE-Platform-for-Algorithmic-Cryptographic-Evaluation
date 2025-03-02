document.addEventListener("DOMContentLoaded", () => {
  // Algorithm Buttons
  const aesCbcButton = document.getElementById("aesCbcButton");
  const aesCbc256Button = document.getElementById("aesCbc256Button");
  const aesGcmButton = document.getElementById("aesGcmButton");
  const aesGcm256Button = document.getElementById("aesGcm256Button");
  const chacha20Button = document.getElementById("chacha20Button");
  const chacha20Poly1305Button = document.getElementById("chacha20Poly1305Button");

  // Benchmark Buttons
  const mediaBenchmarkButton = document.getElementById("mediaBenchmarkButton");
  const processorBenchmarkButton = document.getElementById("processorBenchmarkButton");
  const strengthBenchmarkButton = document.getElementById("strengthBenchmarkButton");
  const pqcBenchmarkButton = document.getElementById("pqcBenchmarkButton");

  // Algorithm Event Listeners
  aesCbcButton.addEventListener("click", () => {
      window.location.href = "/aes_cbc_enc_dec";
  });

  aesCbc256Button.addEventListener("click", () => {
      window.location.href = "/aes_cbc_256_enc_dec";
  });

  aesGcmButton.addEventListener("click", () => {
      window.location.href = "/aes_gcm_enc_dec";
  });

  aesGcm256Button.addEventListener("click", () => {
      window.location.href = "/aes_gcm_256_enc_dec";
  });

  chacha20Button.addEventListener("click", () => {
      window.location.href = "/chacha20_enc_dec";
  });

  chacha20Poly1305Button.addEventListener("click", () => {
      window.location.href = "/chacha20_poly1305_enc_dec";
  });

  // Benchmark Event Listeners
  mediaBenchmarkButton.addEventListener("click", () => {
      window.location.href = "/media";
  });

  processorBenchmarkButton.addEventListener("click", () => {
      window.location.href = "/processor_choosing";
  });

  strengthBenchmarkButton.addEventListener("click", () => {
      window.location.href = "/strength_benchmarking";
  });

  pqcBenchmarkButton.addEventListener("click", () => {
      window.location.href = "/pqc";
  });
});