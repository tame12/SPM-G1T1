function resetErrors(inputs, errorTexts, errorInfo) {
    for (let i = 0; i < inputs.length; i++) {
      inputs[i].classList.remove("error-input");
    }
    for (let i = 0; i < errorTexts.length; i++) {
      errorTexts[i].innerText = "";
    }
    errorInfo.innerText = "";
  }
  
  function checkRequired(value) {
    if (!value) {
      return false;
    }
    value = value.toString().trim();
    if (value === "") {
      return false;
    }
    return true;
  }
  
  function checkTextLengthRange(value, min, max) {
    if (!value) {
      return false;
    }
    value = value.toString().trim();
    const length = value.length;
    if (max && length > max) {
      return false;
    }
    if (min && length < min) {
      return false;
    }
    return true;
  }
  
  
  // validationMovieForm.js
  
  function validateForm() {
  
    const form = document.querySelector('form');
    const message = document.getElementById('info');
  
    const roleNameInput = document.getElementById('role_Name');


  
    const errorroleName = document.getElementById('errorroleName');
    const errorsSummary = document.getElementById('errorsSummary');
  
    let valid = true;
    resetErrors([roleNameInput, descriptionInput], [errorroleName, errordescription], errorsSummary);
  
    if (!checkRequired(roleNameInput.value)) {
      valid = false;
      roleNameInput.classList.add("error-input");
      errorroleName.innerText = "This field is required";
    } else if (!checkTextLengthRange(roleNameInput.value, 1, 50)) {
      valid = false;
      roleNameInput.classList.add("error-input");
      errorroleName.innerText = "You should enter from 1 to 50 letters";
    }
    
  
    if (valid) {
      message.classList.remove('d-none');
    }
  
    if (!valid) {
      errorsSummary.innerText = "Form contains errors";
    }
  
    // return valid;
    return false;
  
  
  }