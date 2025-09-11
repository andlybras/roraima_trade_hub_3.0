document.addEventListener('DOMContentLoaded', function() {
    
    // --- LÓGICA DO CARROSSEL DE DESTAQUES ---
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
            slideInterval = setInterval(nextSlide, 5000); // Muda a cada 5 segundos
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

    // --- LÓGICA DA PAGINAÇÃO AJAX ---
    const carregarMaisBtn = document.getElementById('carregar-mais-btn');
    if (carregarMaisBtn) {
        let page = 2; // Começamos na página 2, pois a 1 já foi carregada
        
        carregarMaisBtn.addEventListener('click', function() {
            fetch(`/noticias/mais-noticias/?page=${page}`)
                .then(response => response.text())
                .then(html => {
                    if (html.trim() !== "") {
                        document.getElementById('lista-noticias-grid').insertAdjacentHTML('beforeend', html);
                        page++;
                    } else {
                        // Se não houver mais notícias, esconde o botão
                        carregarMaisBtn.style.display = 'none';
                    }
                })
                .catch(error => console.error('Erro ao carregar mais notícias:', error));
        });
    }
});