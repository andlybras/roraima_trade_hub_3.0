// CÓDIGO COMPLETO para frontend/gerenciamento_registros/js/form_validation.js

function validateEmailAndCaptchaForm() {
    const emailForm = document.querySelector('.email-form-validation');
    if (!emailForm) return;

    const emailInput = emailForm.querySelector('input[type="email"]');
    const submitButton = emailForm.querySelector('button[type="submit"]');
    const emailError = document.getElementById('email-error-message');
    const recaptchaResponse = document.getElementById('g-recaptcha-response');

    if (!emailInput || !submitButton) return;

    // Regex para validar o formato do e-mail
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    // --- LÓGICA DE VALIDAÇÃO ---

    // 1. Valida o formato do e-mail
    const isEmailValid = emailRegex.test(emailInput.value);

    // 2. Verifica se o reCAPTCHA foi resolvido
    const isRecaptchaSolved = recaptchaResponse && recaptchaResponse.value !== '';

    // 3. Atualiza o campo de input com fundo branco se preenchido
    emailInput.classList.toggle('filled', emailInput.value.length > 0);

    // 4. Mostra a mensagem de erro de e-mail se necessário
    if (emailError) {
        if (emailInput.value.length > 0 && !isEmailValid) {
            emailError.style.display = 'block';
        } else {
            emailError.style.display = 'none';
        }
    }

    // 5. Habilita o botão SOMENTE se AMBOS os critérios forem atendidos
    submitButton.disabled = !(isEmailValid && isRecaptchaSolved);
}

// --- EVENTOS ---

// Gatilho quando a página carrega
document.addEventListener('DOMContentLoaded', function() {
    const emailForm = document.querySelector('.email-form-validation');
    if (!emailForm) return;

    const emailInput = emailForm.querySelector('input[type="email"]');

    // Valida enquanto o usuário digita no campo de e-mail
    if (emailInput) {
        emailInput.addEventListener('input', validateEmailAndCaptchaForm);
        emailInput.addEventListener('blur', validateEmailAndCaptchaForm);
    }
    
    // Inicia a validação no carregamento da página
    validateEmailAndCaptchaForm();
});

// Funções globais que serão chamadas pelo reCAPTCHA quando ele for resolvido ou expirar
window.recaptchaSolvedCallback = function() {
    console.log("reCAPTCHA resolvido. Validando formulário...");
    validateEmailAndCaptchaForm();
};

window.recaptchaExpiredCallback = function() {
    console.log("reCAPTCHA expirado. Validando formulário...");
    validateEmailAndCaptchaForm();
};