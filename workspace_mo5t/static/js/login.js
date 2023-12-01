function validateForm()
 {
  const emailInput = document.querySelector('input[name="email"]');
  const passwordInput = document.querySelector('input[name="password"]');
  const emailError = document.querySelector('#email-error');
  const passwordError = document.querySelector('#password-error');

  emailInput.classList.remove('error');
  passwordInput.classList.remove('error');
  emailError.textContent = '';
  passwordError.textContent = '';

  let isValid = true;

  if (emailInput.value.trim() === '')
   {
    emailInput.classList.add('error');
    emailError.textContent = 'Please enter your email address.';
    isValid = false;
  }

  if (passwordInput.value.trim() === '')
   {
    passwordInput.classList.add('error');
    passwordError.textContent = 'Please enter your password.';
    isValid = false;
  }

  return isValid;
}

const loginForm = document.querySelector('#loginForm');
loginForm.addEventListener('submit', (event) =>
 {
  if (!validateForm()) {
    event.preventDefault();
  }
});
