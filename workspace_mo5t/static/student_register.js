function validateForm()
 {
    const firstNameInput = document.querySelector('input[name="firstName"]');
    const middleNameInput = document.querySelector('input[name="middleName"]');
    const lastNameInput = document.querySelector('input[name="lastName"]');
    const dobInput = document.querySelector('input[name="dateOfBirth"]');
    const emailInput = document.querySelector('input[name="email"]');
    const passwordInput = document.querySelector('input[name="password"]');
    const genderInput = document.querySelector('select[name="gender"]');
    const firstNameError = document.querySelector('#first-name-error');
    const middleNameError = document.querySelector('#middle-name-error');
    const lastNameError = document.querySelector('#last-name-error');
    const dobError = document.querySelector('#dob-error');
    const emailError = document.querySelector('#email-error');
    const passwordError = document.querySelector('#password-error');
    const genderError = document.querySelector('#gender-error');

    firstNameInput.classList.remove('error');
    middleNameInput.classList.remove('error');
    lastNameInput.classList.remove('error');
    dobInput.classList.remove('error');
    emailInput.classList.remove('error');
    passwordInput.classList.remove('error');
    genderInput.classList.remove('error');
    firstNameError.textContent = '';
    middleNameError.textContent = '';
    lastNameError.textContent = '';
    dobError.textContent = '';
    emailError.textContent = '';
    passwordError.textContent = '';
    genderError.textContent = '';

    let isValid = true;

    if (firstNameInput.value.trim() === '') 
    {
        firstNameInput.classList.add('error');
        firstNameError.textContent = 'Please enter your first name.';
        isValid = false;
    }

    if (middleNameInput.value.trim() === '') 
    {
        middleNameInput.classList.add('error');
        middleNameError.textContent = 'Please enter your middle name.';
        isValid = false;
    }

    if (lastNameInput.value.trim() === '')
     {
        lastNameInput.classList.add('error');
        lastNameError.textContent = 'Please enter your last name.';
        isValid = false;
    }

    if (dobInput.value.trim() === '') 
    {
        dobInput.classList.add('error');
        dobError.textContent = 'Please enter your date of birth.';
        isValid = false;
    }

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

    if (genderInput.value === '') 
    {
        genderInput.classList.add('error');
        genderError.textContent = 'Please select your gender.';
        isValid = false;
    }

    return isValid;
}

const registerForm = document.querySelector('#registerForm');
registerForm.addEventListener('submit', (event) => 
{
    event.preventDefault(); 

    if (validateForm()) 
    {
        console.log('Form submitted successfully!');

        setTimeout(() =>
         {
            location.reload();
        }, 1000);
    } 
    else 
    {
        console.log('Form validation failed!');
    }
});
