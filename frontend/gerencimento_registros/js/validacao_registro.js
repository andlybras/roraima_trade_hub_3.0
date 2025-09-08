document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registrationForm');
    if (!form) return;

    const email = form.querySelector('input[name="email"]');
    const email2 = form.querySelector('input[name="email2"]');
    const password = form.querySelector('input[name="password"]');
    const password2 = form.querySelector('input[name="password2"]');
    const submitButton = document.getElementById('submitButton');

    const email2Error = document.getElementById('email2-error');
    const password2Error = document.getElementById('password2-error');

    function validateForm() {
        if (!submitButton) return;

        let isEmailMatch = email.value === email2.value && email.value.length > 0;
        let isPasswordMatch = password.value === password2.value && password.value.length > 0;

        if (email2.value.length > 0) {
            email2Error.textContent = isEmailMatch ? '' : 'Os e-mails não são iguais.';
        }
        if (password2.value.length > 0) {
            password2Error.textContent = isPasswordMatch ? '' : 'As senhas não são iguais.';
        }

        // Simplificando: o botão é habilitado se todos os campos obrigatórios tiverem algum valor.
        // A validação detalhada de senha e outros será feita no backend.
        let allRequiredFilled = true;
        form.querySelectorAll('[required]').forEach(input => {
            if (!input.value) {
                allRequiredFilled = false;
            }
        });

        // O reCAPTCHA é verificado no backend, mas podemos checar se o usuário interagiu
        const recaptchaResponse = form.querySelector('[name="g-recaptcha-response"]');
        const isRecaptchaInteracted = recaptchaResponse ? recaptchaResponse.value !== '' : true;

        submitButton.disabled = !(isEmailMatch && isPasswordMatch && allRequiredFilled && isRecaptchaInteracted);
    }

    form.querySelectorAll('input, select').forEach(input => {
        input.addEventListener('input', validateForm);
    });

    // Um observador para o reCAPTCHA
    const recaptchaContainer = form.querySelector('.g-recaptcha');
    if (recaptchaContainer) {
        const observer = new MutationObserver(validateForm);
        observer.observe(recaptchaContainer, { childList: true, subtree: true });
    }
});