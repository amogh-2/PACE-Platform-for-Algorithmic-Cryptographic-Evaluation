
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
document.addEventListener('DOMContentLoaded', () => {
    const aesButton = document.getElementById('aesButton');
    const chacha20Button = document.getElementById('chacha20Button');

    aesButton.addEventListener('click', () => {
        sendAlgorithm('aes');
    });

    chacha20Button.addEventListener('click', () => {
        sendAlgorithm('chacha20');
    });
});

function sendAlgorithm(algorithm) {
    fetch('/encrypt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ algorithm: algorithm })
    })
    .then(response => response.json())
    .then(data => console.log('Algorithm set:', data))
    .catch(error => console.error('Error:', error));
}
