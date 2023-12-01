function validateForm() 
{
    const codeInput = document.querySelector('input[name="code"]');
    const codeError = document.querySelector('#code-error');
  
    codeInput.classList.remove('error');
    codeError.textContent = '';
  
    let isValid = true;
  
    if (codeInput.value.trim() === '')
     {
      codeInput.classList.add('error');
      codeError.textContent = 'Please enter the verification code.';
      isValid = false;
    }
  
    return isValid;
  }
  
  const verifyCodeForm = document.querySelector('#verifyCodeForm');
  verifyCodeForm.addEventListener('submit', (event) => 
  {
    if (!validateForm())
     {
      event.preventDefault();
    } 
    else 
    {
      // ezay b2a hanb3at el code ya regaalah , aywa s7 han3mel 3a2d m3 etisalat aw vodafone hahhahahaha , asef!.
      
    }
  });
  