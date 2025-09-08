// Arquivo: home.js
document.addEventListener('DOMContentLoaded', function() {
    const heroSlides = document.querySelectorAll('.slide-hero');
    if (heroSlides.length > 1) {
        let currentSlide = 0;
        setInterval(() => {
            heroSlides[currentSlide].classList.remove('is-active');
            currentSlide = (currentSlide + 1) % heroSlides.length;
            heroSlides[currentSlide].classList.add('is-active');
        }, 8000);
    }
});