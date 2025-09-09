document.addEventListener('DOMContentLoaded', function() {
    const userMenuButton = document.getElementById('userMenuButton');
    if (userMenuButton) {
        const dropdownMenu = userMenuButton.nextElementSibling;
        userMenuButton.addEventListener('click', function(event) {
            event.stopPropagation();
            dropdownMenu.classList.toggle('show');
        });
        window.addEventListener('click', function(event) {
            if (!userMenuButton.contains(event.target)) {
                dropdownMenu.classList.remove('show');
            }
        });
    }
});