document.addEventListener('DOMContentLoaded', function() {
    
    const carousel = document.getElementById('destaques-carousel');
    if (carousel) {
        const slides = carousel.querySelectorAll('.destaque-slide');
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');
        let currentSlide = 0;
        let slideInterval;

        function showSlide(index) {
            slides.forEach((slide, i) => {
                slide.classList.remove('active');
                if (i === index) {
                    slide.classList.add('active');
                }
            });
        }

        function nextSlide() {
            currentSlide = (currentSlide + 1) % slides.length;
            showSlide(currentSlide);
        }

        function prevSlide() {
            currentSlide = (currentSlide - 1 + slides.length) % slides.length;
            showSlide(currentSlide);
        }

        function startCarousel() {
            slideInterval = setInterval(nextSlide, 10000);
        }

        function stopCarousel() {
            clearInterval(slideInterval);
        }

        if (slides.length > 1) {
            nextBtn.addEventListener('click', () => {
                nextSlide();
                stopCarousel();
                startCarousel();
            });
            prevBtn.addEventListener('click', () => {
                prevSlide();
                stopCarousel();
                startCarousel();
            });
            startCarousel();
        }
    }

    const carregarMaisBtn = document.getElementById('carregar-mais-btn');
    if (carregarMaisBtn) {
        let page = 2;
        let isLoading = false;

        carregarMaisBtn.addEventListener('click', function() {
            if (isLoading) return;
            
            isLoading = true;
            carregarMaisBtn.textContent = 'Carregando...';

            fetch(`/noticias/mais-noticias/?page=${page}`)
                .then(response => response.text())
                .then(html => {
                    if (html.trim() !== "") {
                        document.getElementById('lista-noticias-grid').insertAdjacentHTML('beforeend', html);
                        page++;
                        carregarMaisBtn.textContent = 'Carregar Mais Notícias';
                        isLoading = false;
                    } else {
                        carregarMaisBtn.textContent = 'Fim das Notícias';
                        carregarMaisBtn.disabled = true;
                    }
                })
                .catch(error => {
                    console.error('Erro ao carregar mais notícias:', error);
                    isLoading = false;
                    carregarMaisBtn.textContent = 'Erro ao carregar';
                });
        });
    }
});