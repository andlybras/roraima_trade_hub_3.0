// frontend/gerenciamento_destino/js/galeria_lightbox.js
document.addEventListener('DOMContentLoaded', function() {
    const galeriaImagens = document.querySelectorAll('.galeria-imagem');
    if (galeriaImagens.length === 0) return;

    const lightbox = document.getElementById('lightbox');
    const lightboxImage = document.getElementById('lightbox-image');
    const lightboxClose = document.getElementById('lightbox-close');
    const lightboxPrev = document.getElementById('lightbox-prev');
    const lightboxNext = document.getElementById('lightbox-next');
    let currentIndex = 0;

    function openLightbox(index) {
        currentIndex = index;
        lightboxImage.src = galeriaImagens[currentIndex].src;
        lightbox.style.display = 'flex';
    }

    function closeLightbox() {
        lightbox.style.display = 'none';
    }

    function showPrev() {
        currentIndex = (currentIndex > 0) ? currentIndex - 1 : galeriaImagens.length - 1;
        lightboxImage.src = galeriaImagens[currentIndex].src;
    }

    function showNext() {
        currentIndex = (currentIndex < galeriaImagens.length - 1) ? currentIndex + 1 : 0;
        lightboxImage.src = galeriaImagens[currentIndex].src;
    }

    galeriaImagens.forEach((img, index) => {
        img.addEventListener('click', () => openLightbox(index));
    });

    lightboxClose.addEventListener('click', closeLightbox);
    lightboxPrev.addEventListener('click', showPrev);
    lightboxNext.addEventListener('click', showNext);

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeLightbox();
    });
});