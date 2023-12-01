function validateForm()
{
  const emailInput = document.querySelector('input[name="email"]');
  const emailError = document.querySelector('#email-error');

  emailInput.classList.remove('error');
  emailError.textContent = '';

  let isValid = true;

  if (emailInput.value.trim() === '')
  {
    emailInput.classList.add('error');
    emailError.textContent = 'Please enter your email address.';
    isValid = false;
  }

  return isValid;
}

const forgotPasswordForm = document.querySelector('#forgotPasswordForm');
forgotPasswordForm.addEventListener('submit', (event) =>
{
  if (!validateForm()) 
  {
    event.preventDefault();
  }
});
