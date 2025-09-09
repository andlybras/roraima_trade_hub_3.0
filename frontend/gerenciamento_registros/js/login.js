// Arquivo: frontend/gerenciamento_registros/js/login.js

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    if (!loginForm) return;

    const usernameInput = document.querySelector('input[name="username"]');
    const passwordInput = document.querySelector('input[name="password"]');
    const loginButton = document.getElementById('loginButton');
    const formMessage = document.getElementById('form-message');

    function checkLoginForm() {
        if (!usernameInput || !passwordInput || !loginButton) return;
        
        // MUDANÇA 1: Adiciona/remove a classe 'filled' dinamicamente
        usernameInput.classList.toggle('filled', usernameInput.value.length > 0);
        passwordInput.classList.toggle('filled', passwordInput.value.length > 0);

        const isUsernameFilled = usernameInput.value.length > 0;
        // MUDANÇA 2: Verifica se a senha tem no mínimo 8 caracteres
        const isPasswordValid = passwordInput.value.length >= 8;

        loginButton.disabled = !(isUsernameFilled && isPasswordValid);
    }

    function showTemporaryMessage(messageElement) {
        if (messageElement) {
            // Atualiza a mensagem se a senha for o problema
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

    // Adicionamos 'blur' para garantir que o estilo 'filled' seja aplicado
    // mesmo se o usuário apenas preencher e sair do campo.
    usernameInput.addEventListener('input', checkLoginForm);
    usernameInput.addEventListener('blur', checkLoginForm); 
    
    passwordInput.addEventListener('input', checkLoginForm);
    passwordInput.addEventListener('blur', checkLoginForm);
    
    // Verifica o formulário no carregamento da página
    checkLoginForm();
});