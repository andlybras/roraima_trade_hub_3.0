// Arquivo: frontend/gerenciamento_home/js/dropdown.js
document.addEventListener('DOMContentLoaded', function() {
    const userMenuButton = document.getElementById('userMenuButton');
    if (userMenuButton) {
        const dropdownMenu = userMenuButton.nextElementSibling;

        userMenuButton.addEventListener('click', function(event) {
            event.stopPropagation(); // Impede que o clique feche o menu imediatamente
            dropdownMenu.classList.toggle('show');
        });

        // Fecha o dropdown se o usuário clicar fora dele
        window.addEventListener('click', function(event) {
            if (!userMenuButton.contains(event.target)) {
                dropdownMenu.classList.remove('show');
            }
        });
    }
});