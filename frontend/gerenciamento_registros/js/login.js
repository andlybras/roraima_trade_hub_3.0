document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    if (!loginForm) return;

    const usernameInput = document.querySelector('input[name="username"]');
    const passwordInput = document.querySelector('input[name="password"]');
    const loginButton = document.getElementById('loginButton');
    const formMessage = document.getElementById('form-message');

    function checkLoginForm() {
        if (!usernameInput || !passwordInput || !loginButton) return;
        
        usernameInput.classList.toggle('filled', usernameInput.value.length > 0);
        passwordInput.classList.toggle('filled', passwordInput.value.length > 0);

        const isUsernameFilled = usernameInput.value.length > 0;
        const isPasswordValid = passwordInput.value.length >= 8;

        loginButton.disabled = !(isUsernameFilled && isPasswordValid);
    }

    function showTemporaryMessage(messageElement) {
        if (messageElement) {
            if (usernameInput.value.length > 0 && passwordInput.value.length > 0 && passwordInput.value.length < 8) {
                messageElement.textContent = "A senha deve ter no mínimo 8 caracteres.";
            } else {
                messageElement.textContent = "Por favor, preencha todos os campos.";
            }
            messageElement.classList.add('show');
            setTimeout(() => {
                messageElement.classList.remove('show');
            }, 3000);
        }
    }

    loginButton.addEventListener('click', function(event) {
        if (loginButton.disabled) {
            event.preventDefault();
            showTemporaryMessage(formMessage);
        }
    });

    usernameInput.addEventListener('input', checkLoginForm);
    usernameInput.addEventListener('blur', checkLoginForm); 
    passwordInput.addEventListener('input', checkLoginForm);
    passwordInput.addEventListener('blur', checkLoginForm);

    checkLoginForm();
});