// VERSÃO FINAL - frontend/gerenciamento_registros/js/registro.js

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registrationForm');
    if (!form) return;

    // --- Seletores ---
    const submitButton = document.getElementById('submitButton');
    const passwordInput = document.getElementById('id_password1');
    const emailInput = document.getElementById('id_email');
    const email2Input = document.getElementById('id_email2');
    const password2Input = document.getElementById('id_password2');
    const passwordFeedback = document.getElementById('password-feedback');
    const emailError = document.getElementById('email-error');
    const email2Error = document.getElementById('email2-error');
    const password2Error = document.getElementById('password2-error');

    // --- Regras da Senha e Ícones ---
    const passwordRules = [
        { regex: /.{8,}/, text: "Pelo menos 8 caracteres" },
        { regex: /[A-Z]/, text: "Pelo menos uma letra maiúscula" },
        { regex: /[a-z]/, text: "Pelo menos uma letra minúscula" },
        { regex: /[0-9]/, text: "Pelo menos um número" },
    ];
    const iconError = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.647a.5.5 0 0 0-.708-.708L8 7.293z"/></svg>';
    const iconSuccess = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/></svg>';

    const updatePasswordUI = () => {
        if (!passwordFeedback || !passwordInput) return;
        const rulesContainer = passwordFeedback.querySelector('.validation-rules');
        if (!rulesContainer) return;
        if (rulesContainer.childElementCount === 0) {
            passwordRules.forEach((rule, index) => {
                const ruleDiv = document.createElement('div');
                ruleDiv.id = `rule-${index}`;
                ruleDiv.innerHTML = `<span class="validation-icon">${iconError}</span><span>${rule.text}</span>`;
                rulesContainer.appendChild(ruleDiv);
            });
        }
        passwordRules.forEach((rule, index) => {
            const ruleDiv = document.getElementById(`rule-${index}`);
            const iconSpan = ruleDiv.querySelector('.validation-icon');
            const isValid = rule.regex.test(passwordInput.value);
            ruleDiv.className = isValid ? 'valid' : 'invalid';
            iconSpan.innerHTML = isValid ? iconSuccess : iconError;
        });
    };

    const validateForm = () => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
        let isAllValid = true;

        // Valida cada campo de texto individualmente
        form.querySelectorAll('input[type="text"], input[type="email"], input[type="password"]').forEach(field => {
            if (!field.value.trim()) isAllValid = false;
            field.classList.toggle('filled', field.value.length > 0);
        });

        // Valida rádio
        const tipoPerfilRadios = form.querySelectorAll('input[name="tipo_perfil"]');
        if (tipoPerfilRadios.length > 0 && !Array.from(tipoPerfilRadios).some(r => r.checked)) {
            isAllValid = false;
        }

        // Valida formato e confirmação de email
        if (!emailInput || !emailRegex.test(emailInput.value)) isAllValid = false;
        if (!email2Input || emailInput.value !== email2Input.value) isAllValid = false;

        // Valida complexidade e confirmação de senha
        if (!passwordInput || !passwordRules.every(rule => rule.regex.test(passwordInput.value))) isAllValid = false;
        if (!password2Input || passwordInput.value !== password2Input.value) isAllValid = false;
        
        // Valida reCAPTCHA
        const recaptcha = form.querySelector('[name="g-recaptcha-response"]');
        if (!recaptcha || !recaptcha.value) isAllValid = false;

        submitButton.disabled = !isAllValid;
    };

    const handleFieldFeedback = (field) => {
        if (field.id === 'id_password1') updatePasswordUI();

        if (field.id === 'id_email' && emailError) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            emailError.textContent = (field.value.length > 0 && !emailRegex.test(field.value)) ? 'O formato do e-mail é inválido.' : '';
        }
        if (field.id === 'id_email2' && email2Error) {
            email2Error.textContent = (emailInput && field.value.length > 0 && emailInput.value !== field.value) ? 'Os e-mails não coincidem.' : '';
        }
        if (field.id === 'id_password2' && password2Error) {
            password2Error.textContent = (passwordInput && field.value.length > 0 && passwordInput.value !== field.value) ? 'As senhas não coincidem.' : '';
        }
    };

    // --- Event Listeners ---
    form.addEventListener('input', (event) => {
        handleFieldFeedback(event.target);
        validateForm();
    });
    form.addEventListener('change', validateForm); // Para radios

    window.recaptchaCallback = validateForm;
    window.recaptchaExpiredCallback = validateForm;

    // --- Inicialização ---
    updatePasswordUI();
    validateForm();
});