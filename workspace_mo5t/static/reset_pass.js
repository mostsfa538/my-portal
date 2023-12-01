function validateForm() 
{
    const newPasswordInput = document.querySelector('input[name="newPassword"]');
    const confirmPasswordInput = document.querySelector('input[name="confirmPassword"]');
    const newPasswordError = document.querySelector('#new-password-error');
    const confirmPasswordError = document.querySelector('#confirm-password-error');
  
    newPasswordInput.classList.remove('error');
    confirmPasswordInput.classList.remove('error');
    newPasswordError.textContent = '';
    confirmPasswordError.textContent = '';
  
    let isValid = true;
  
    if (newPasswordInput.value.trim() === '')
     {
      newPasswordInput.classList.add('error');
      newPasswordError.textContent = 'Please enter a new password.';
      isValid = false;
    }
  
    if (confirmPasswordInput.value.trim() === '') 
    {
      confirmPasswordInput.classList.add('error');
      confirmPasswordError.textContent = 'Please confirm your new password.';
      isValid = false;
    }
  
    if (newPasswordInput.value !== confirmPasswordInput.value)
     {
      newPasswordInput.classList.add('error');
      confirmPasswordInput.classList.add('error');
      confirmPasswordError.textContent = 'Passwords do not match.';
      isValid = false;
    }
  
    return isValid;
  }
  
  const resetPasswordForm = document.querySelector('#resetPasswordForm');
  resetPasswordForm.addEventListener('submit', (event) => 
  {
    if (!validateForm()) 
    {
      event.preventDefault();
   
    }
  });
  