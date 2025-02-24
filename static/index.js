document.addEventListener('DOMContentLoaded', () => {
    const aes_cbcButton = document.getElementById('aes_cbcButton');
    const aesGcmButton = document.getElementById('aesGcmButton');
    const chacha20Button = document.getElementById('chacha20Button');

    aes_cbcButton.addEventListener('click', () => {
        window.location.href = '/aes_cbc_enc_dec';
    });

    aesGcmButton.addEventListener('click', () => {
        window.location.href = '/aes_gcm_enc_dec';
    });

    chacha20Button.addEventListener('click', () => {
        window.location.href = '/chacha20_enc_dec';
    });
});