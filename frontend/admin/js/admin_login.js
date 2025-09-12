document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    if (!loginForm) return;

    const usernameInput = document.querySelector('input[name="username"]');
    const passwordInput = document.querySelector('input[name="password"]');
    const loginButton = document.getElementById('loginButton');

    function checkLoginForm() {
        if (!usernameInput || !passwordInput || !loginButton) return;

        usernameInput.classList.toggle('filled', usernameInput.value.length > 0);
        passwordInput.classList.toggle('filled', passwordInput.value.length > 0);

        const isUsernameFilled = usernameInput.value.length > 0;
        const isPasswordValid = passwordInput.value.length >= 8; 
        
        loginButton.disabled = !(isUsernameFilled && isPasswordValid);
    }

    if(usernameInput) {
        usernameInput.addEventListener('input', checkLoginForm);
        usernameInput.addEventListener('blur', checkLoginForm);
    }
    
    if(passwordInput) {
        passwordInput.addEventListener('input', checkLoginForm);
        passwordInput.addEventListener('blur', checkLoginForm);
    }

    checkLoginForm();
});