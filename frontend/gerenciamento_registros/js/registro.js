document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registrationForm');
    if (!form) return;
    const submitButton = document.getElementById('submitButton');
    const allInputs = Array.from(form.querySelectorAll('input, select, textarea'));
    const password = document.getElementById('id_password1');
    const password2 = document.getElementById('id_password2');
    const email = document.getElementById('id_email');
    const email2 = document.getElementById('id_email2');
    const passwordFeedback = document.getElementById('password-feedback');
    const email2Error = document.getElementById('email2-error');
    const password2Error = document.getElementById('password2-error');
    const passwordRules = [
        { regex: /.{8,}/, text: "Pelo menos 8 caracteres" },
        { regex: /[A-Z]/, text: "Pelo menos uma letra maiúscula" },
        { regex: /[a-z]/, text: "Pelo menos uma letra minúscula" },
        { regex: /[0-9]/, text: "Pelo menos um número" },
    ];
    const iconError = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293z"/></svg>';
    const iconSuccess = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/></svg>';

    function updatePasswordUI() {
        if (!passwordFeedback) return;
        const rulesContainer = passwordFeedback.querySelector('.validation-rules');
        if(!rulesContainer) return;

        if(rulesContainer.childElementCount === 0) {
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
            if (rule.regex.test(password.value)) {
                ruleDiv.classList.replace('invalid', 'valid');
                iconSpan.innerHTML = iconSuccess;
            } else {
                ruleDiv.classList.replace('valid', 'invalid');
                iconSpan.innerHTML = iconError;
            }
        });
    }

    function checkConfirmation(field1, field2, errorElement, message) {
        if (field1.value && field2.value && field1.value !== field2.value) {
            errorElement.textContent = message;
        } else {
            errorElement.textContent = '';
        }
    }

    function validateForm() {
        let isFormValid = true;

        allInputs.forEach(input => {
            if (input.type === 'hidden' || input.name === 'g-recaptcha-response') return;

            if (input.type === 'radio') {
                const radioGroup = form.querySelectorAll(`input[name="${input.name}"]`);
                if (!Array.from(radioGroup).some(radio => radio.checked)) {
                    isFormValid = false;
                }
            } else if (!input.value.trim()) {
                isFormValid = false;
            }
        });

        passwordRules.forEach(rule => {
            if (password && !rule.regex.test(password.value)) {
                isFormValid = false;
            }
        });

        if (email && email2 && email.value !== email2.value) isFormValid = false;
        if (password && password2 && password.value !== password2.value) isFormValid = false;

        const recaptchaResponse = form.querySelector('[name="g-recaptcha-response"]');
        if (!recaptchaResponse || recaptchaResponse.value === '') {
            isFormValid = false;
        }

        submitButton.disabled = !isFormValid;
    }

    allInputs.forEach(input => {
        input.addEventListener('input', validateForm);
        input.addEventListener('change', validateForm);
    });

    if (password) password.addEventListener('input', updatePasswordUI);
    if (email && email2) email2.addEventListener('input', () => checkConfirmation(email, email2, email2Error, 'Os e-mails não são iguais.'));
    if (password && password2) password2.addEventListener('input', () => checkConfirmation(password, password2, password2Error, 'As senhas não são iguais.'));

    window.recaptchaCallback = function() {
        validateForm();
    };
    updatePasswordUI();
    validateForm();
});