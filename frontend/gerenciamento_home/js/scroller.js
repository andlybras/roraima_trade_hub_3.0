// Arquivo: scroller.js
document.addEventListener('DOMContentLoaded', () => {
    const scrollers = document.querySelectorAll(".carrossel-infinito");

    // Se o usuário não tiver a opção de movimento reduzido ativada, adicionamos a animação
    if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        scrollers.forEach((scroller) => {
            addAnimation(scroller);
        });
    }

    function addAnimation(scroller) {
        const scrollerInner = scroller.querySelector(".carrossel-infinito-faixa");
        const scrollerContent = Array.from(scrollerInner.children);

        // Se não houver conteúdo, não faz nada
        if (scrollerContent.length === 0) return;

        // Duplica cada item e adiciona ao final da faixa
        scrollerContent.forEach(item => {
            const duplicatedItem = item.cloneNode(true);
            duplicatedItem.setAttribute("aria-hidden", true);
            scrollerInner.appendChild(duplicatedItem);
        });

        // Habilita a animação via CSS
        scroller.dataset.animacao = "true";
    }
});