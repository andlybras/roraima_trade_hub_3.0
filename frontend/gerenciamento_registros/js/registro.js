// VERSÃO FINAL E COMPLETA de frontend/gerenciamento_registros/js/registro.js

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registrationForm');
    if (!form) return;

    // --- Seletores dos Elementos ---
    const allInputs = Array.from(form.querySelectorAll('input, select, textarea'));
    const submitButton = document.getElementById('submitButton');
    const passwordInput = document.getElementById('id_password1');
    const password2Input = document.getElementById('id_password2');
    const emailInput = document.getElementById('id_email');
    const email2Input = document.getElementById('id_email2');
    
    const emailError = document.getElementById('email-error'); // Usaremos este ID para o formato
    const email2Error = document.getElementById('email2-error');
    const password2Error = document.getElementById('password2-error');
    const passwordFeedback = document.getElementById('password-feedback');
    
    // --- ÍCONES E REGRAS DA SENHA (RESTAURADOS) ---
    const passwordRules = [
        { regex: /.{8,}/, text: "Pelo menos 8 caracteres" },
        { regex: /[A-Z]/, text: "Pelo menos uma letra maiúscula" },
        { regex: /[a-z]/, text: "Pelo menos uma letra minúscula" },
        { regex: /[0-9]/, text: "Pelo menos um número" },
    ];
    const iconError = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.647a.5.5 0 0 0-.708-.708L8 7.293z"/></svg>';
    const iconSuccess = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/></svg>';

    // --- FUNÇÕES DE FEEDBACK VISUAL ---

    function updatePasswordUI() {
        if (!passwordFeedback || !passwordInput) return;
        const rulesContainer = passwordFeedback.querySelector('.validation-rules');
        if (!rulesContainer) return;

        if (rulesContainer.childElementCount === 0) {
            passwordRules.forEach((rule, index) => {
                const ruleDiv = document.createElement('div');
                ruleDiv.id = `rule-${index}`;
                ruleDiv.classList.add('invalid');
                ruleDiv.innerHTML = `<span class="validation-icon">${iconError}</span><span>${rule.text}</span>`;
                rulesContainer.appendChild(ruleDiv);
            });
        }

        passwordRules.forEach((rule, index) => {
            const ruleDiv = document.getElementById(`rule-${index}`);
            const iconSpan = ruleDiv.querySelector('.validation-icon');
            if (rule.regex.test(passwordInput.value)) {
                ruleDiv.classList.replace('invalid', 'valid');
                iconSpan.innerHTML = iconSuccess;
            } else {
                ruleDiv.classList.replace('valid', 'invalid');
                iconSpan.innerHTML = iconError;
            }
        });
    }

    function checkEmailFormat() {
        if (!emailInput || !emailError) return;
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (emailInput.value.length > 0 && !emailRegex.test(emailInput.value)) {
            emailError.textContent = 'O formato do e-mail é inválido.';
        } else {
            emailError.textContent = '';
        }
    }

    function checkConfirmation(field1, field2, errorElement, message) {
        if (field1 && field2 && field2.value.length > 0 && field1.value !== field2.value) {
            errorElement.textContent = message;
        } else {
            errorElement.textContent = "";
        }
    }

    function addFilledClassToAllFields() {
        allInputs.forEach(input => {
            if (input.type !== 'radio' && input.type !== 'checkbox' && input.name !== 'g-recaptcha-response') {
                input.classList.toggle('filled', input.value.length > 0);
            }
        });
    }

    // --- FUNÇÃO PRINCIPAL DE VALIDAÇÃO (ROBUSTA) ---
    function validateForm() {
        let isFormValid = true;

        // Critério 1: Todos os campos (exceto radio e hidden) devem estar preenchidos
        allInputs.forEach(input => {
            if (!['hidden', 'radio', 'checkbox'].includes(input.type) && input.name !== 'g-recaptcha-response' && !input.value.trim()) {
                isFormValid = false;
            }
        });

        // Critério 2: Um botão de rádio de perfil deve estar selecionado (se existir)
        const tipoPerfilRadios = form.querySelectorAll('input[name="tipo_perfil"]');
        if (tipoPerfilRadios.length > 0 && !Array.from(tipoPerfilRadios).some(r => r.checked)) {
            isFormValid = false;
        }

        // Critério 3: O e-mail deve ter formato válido
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (emailInput && !emailRegex.test(emailInput.value)) {
            isFormValid = false;
        }

        // Critério 4: As confirmações de e-mail e senha devem ser iguais
        if (emailInput && email2Input && emailInput.value !== email2Input.value) isFormValid = false;
        if (passwordInput && password2Input && passwordInput.value !== password2Input.value) isFormValid = false;

        // Critério 5: A senha deve passar em todas as regras de complexidade
        if (passwordInput) {
            for (const rule of passwordRules) {
                if (!rule.regex.test(passwordInput.value)) {
                    isFormValid = false;
                    break;
                }
            }
        }
        
        // Critério 6: O reCAPTCHA deve estar resolvido
        const recaptchaResponse = form.querySelector('[name="g-recaptcha-response"]');
        if (!recaptchaResponse || !recaptchaResponse.value) {
            isFormValid = false;
        }

        // --- ATIVAÇÃO DO BOTÃO ---
        if (submitButton) {
            submitButton.disabled = !isFormValid;
        }
    }

    // --- VINCULANDO TODOS OS EVENTOS ---

    allInputs.forEach(input => {
        // 'input' para feedback instantâneo enquanto digita
        input.addEventListener('input', () => {
            addFilledClassToAllFields();
            if (input.id === 'id_password1') updatePasswordUI();
            if (input.id === 'id_email') checkEmailFormat();
            if (input.id === 'id_email2') checkConfirmation(emailInput, email2Input, email2Error, 'Os e-mails não coincidem.');
            if (input.id === 'id_password2') checkConfirmation(passwordInput, password2Input, password2Error, 'As senhas não coincidem.');
            validateForm();
        });
        // 'change' é crucial para botões de rádio
        input.addEventListener('change', validateForm);
    });

    // Callbacks para o reCAPTCHA
    window.recaptchaCallback = validateForm;
    window.recaptchaExpiredCallback = validateForm;

    // Inicialização no carregamento da página
    addFilledClassToAllFields();
    updatePasswordUI();
    validateForm();
});