// Arquivo: header.js
// Este script monitora a rolagem da página e aplica uma classe ao cabeçalho.

document.addEventListener('DOMContentLoaded', () => {
    const header = document.querySelector('.cabecalho-principal');

    if (header) {
        window.addEventListener('scroll', () => {
            // Se o usuário rolar mais de 50 pixels para baixo
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });
    }
});