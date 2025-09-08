document.addEventListener('DOMContentLoaded', () => {
    const scrollers = document.querySelectorAll(".carrossel-infinito");
    if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        scrollers.forEach((scroller) => {
            addAnimation(scroller);
        });
    }
    function addAnimation(scroller) {
        const scrollerInner = scroller.querySelector(".carrossel-infinito-faixa");
        const scrollerContent = Array.from(scrollerInner.children);
        if (scrollerContent.length === 0) return;
        scrollerContent.forEach(item => {
            const duplicatedItem = item.cloneNode(true);
            duplicatedItem.setAttribute("aria-hidden", true);
            scrollerInner.appendChild(duplicatedItem);
        });
        scroller.dataset.animacao = "true";
    }
});