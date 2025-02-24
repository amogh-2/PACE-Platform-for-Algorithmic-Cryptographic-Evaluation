document.addEventListener('DOMContentLoaded', () => {
    const aesButton = document.getElementById('aesButton');
    const chacha20Button = document.getElementById('chacha20Button');

    aesButton.addEventListener('click', () => {
        window.location.href = '/aes_enc_dec';
    });

    chacha20Button.addEventListener('click', () => {
        window.location.href = '/chacha20_enc_dec';
    });
});