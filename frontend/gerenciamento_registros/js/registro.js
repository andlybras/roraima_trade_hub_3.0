document.addEventListener('DOMContentLoaded', function() {
    const registrationForm = document.getElementById('registrationForm');
    if (!registrationForm) return;

    const tipoPerfilRadios = document.querySelectorAll('input[name="tipo_perfil"]');
    const email = document.getElementById('id_email');
    const email2 = document.getElementById('id_email2');
    const password = document.getElementById('id_password1');
    const password2 = document.getElementById('id_password2');
    const submitButton = document.getElementById('submitButton');
    const emailError = document.getElementById('email-error');
    const email2Error = document.getElementById('email2-error');
    const password2Error = document.getElementById('password2-error');
    const passwordFeedback = document.getElementById('password-feedback');

    const iconError = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293z"/></svg>';
    const iconSuccess = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/></svg>';

    const passwordRules = [
        { regex: /.{8,}/, text: "Pelo menos 8 caracteres" },
        { regex: /[A-Z]/, text: "Pelo menos uma letra maiúscula" },
        { regex: /[a-z]/, text: "Pelo menos uma letra minúscula" },
        { regex: /[0-9]/, text: "Pelo menos um número" },
    ];

    const rulesContainer = passwordFeedback.querySelector('.validation-rules');
    rulesContainer.innerHTML = '';
    passwordRules.forEach((rule, index) => {
        const ruleDiv = document.createElement('div');
        ruleDiv.id = `rule-${index}`;
        ruleDiv.classList.add('invalid');
        ruleDiv.innerHTML = `<span class="validation-icon">${iconError}</span><span>${rule.text}</span>`;
        rulesContainer.appendChild(ruleDiv);
    });

    const validateEmailFormat = () => {
        if (!email) return false;
        const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value);
        email.classList.toggle('valid', isValid);
        email.classList.toggle('invalid', !isValid && email.value.length > 0);
        emailError.textContent = (!isValid && email.value.length > 0) ? "Formato de e-mail inválido." : "";
        return isValid;
    };

    const validateEmailConfirmation = () => {
        if (!email || !email2) return false;
        const isValid = email.value === email2.value && email.value.length > 0;
        email2.classList.toggle('valid', isValid);
        email2.classList.toggle('invalid', !isValid && email2.value.length > 0);
        email2Error.textContent = (!isValid && email2.value.length > 0) ? "Os e-mails não são iguais." : "";
        return isValid;
    };

    const validatePasswordStrength = () => {
        if (!password) return false;
        let allRulesValid = true;
        passwordRules.forEach((rule, index) => {
            const ruleDiv = document.getElementById(`rule-${index}`);
            const iconSpan = ruleDiv.querySelector('.validation-icon');
            if (rule.regex.test(password.value)) {
                ruleDiv.classList.replace('invalid', 'valid');
                iconSpan.innerHTML = iconSuccess;
            } else {
                ruleDiv.classList.replace('valid', 'invalid');
                iconSpan.innerHTML = iconError;
                allRulesValid = false;
            }
        });
        password.classList.toggle('valid', allRulesValid);
        password.classList.toggle('invalid', !allRulesValid && password.value.length > 0);
        return allRulesValid;
    };

    const validatePasswordConfirmation = () => {
        if (!password || !password2) return false;
        const isValid = password.value === password2.value && password.value.length > 0;
        password2.classList.toggle('valid', isValid);
        password2.classList.toggle('invalid', !isValid && password2.value.length > 0);
        password2Error.textContent = (!isValid && password2.value.length > 0) ? "As senhas não são iguais." : "";
        return isValid;
    };

    const checkFormValidity = () => {
        const isUserTypeSelected = Array.from(tipoPerfilRadios).some(radio => radio.checked);
        const isEmailValid = email.classList.contains('valid');
        const isEmail2Valid = email2.classList.contains('valid');
        const isPasswordValid = password.classList.contains('valid');
        const isPassword2Valid = password2.classList.contains('valid');
        const recaptchaResponse = registrationForm.querySelector('[name="g-recaptcha-response"]');
        const isRecaptchaValid = recaptchaResponse && recaptchaResponse.value !== '';
        
        submitButton.disabled = !(isUserTypeSelected && isEmailValid && isEmail2Valid && isPasswordValid && isPassword2Valid && isRecaptchaValid);
    };

    const allInputs = [email, email2, password, password2];
    allInputs.forEach(input => {
        input.addEventListener('input', () => {
            validateEmailFormat();
            validateEmailConfirmation();
            validatePasswordStrength();
            validatePasswordConfirmation();
            checkFormValidity();
        });
    });

    tipoPerfilRadios.forEach(radio => radio.addEventListener('change', checkFormValidity));

    window.recaptchaCallback = function() {
        checkFormValidity();
    };
});