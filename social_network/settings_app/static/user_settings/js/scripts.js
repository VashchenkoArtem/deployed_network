document.addEventListener('DOMContentLoaded', function () {
    const buttonRedact = document.querySelector(".edit-2");
    const screenDiv = document.querySelector(".screen");
    const buttonSave = document.querySelector(".save-info-button");
    const eyeImages = document.querySelectorAll(".eye-img");
    const editButtons = document.querySelectorAll('.edit-info-button');
    const editProfileCard = document.querySelector(".edit-profile-card");
    const defaultCard = document.querySelector(".default-profile-card");
    const inputImage = document.querySelector(".change-avatar");
    const imageAvatar = document.querySelector('.redact-user-img');
    const editPassword = document.querySelector(".edit-password-div");
    const passwordsDiv = document.querySelector(".passwords-div");
    const inputDivPassword = document.querySelector(".input-div-edit-password");
    const editSavedPassword = document.querySelector(".edit-save-password");
    const buttonPhoto = document.querySelector(".edit-photo-button");

    
    for (let count = 0; count < eyeImages.length; count++){
        let eyeImage = eyeImages[count];
        let input = document.getElementById(eyeImage.id)
        eyeImage.addEventListener("click", (event)=>{
            if (eyeImage.src.includes("eye.png")){
                eyeImage.src += "/../eye_close.png"
                
                input.type = "password"
            }
            else if (eyeImage.src.includes("eye_close.png")){
                eyeImage.src += "/../eye.png"
                input.type = "text"
            }
        })
        if (input.name.includes("password1") || input.name.includes("password2") || input.name.includes("password")){
            eyeImage.src += "/../eye_close.png"
        }
    }

    buttonRedact.addEventListener("click", ()=>{
        screenDiv.classList.toggle("hidden")
        buttonRedact.classList.toggle("hidden")
        buttonSave.classList.toggle("hidden")
    })
    for (let count = 0; count < editButtons.length; count ++){
        let editButton = editButtons[count];
        editButton.addEventListener('click', function(){
            let inputHidden = document.getElementById("hiddenInput");
            inputHidden.value = "verification-code"
            editPassword.classList.toggle("hidden");
            passwordsDiv.classList.toggle("hidden");
            inputDivPassword.classList.toggle("hidden");
    })
    }
    buttonPhoto.addEventListener("click", ()=>{
        editProfileCard.classList.toggle("hidden");
        defaultCard.classList.toggle("hidden");
    })
    inputImage.addEventListener('change', function() {
        const image = inputImage.files[0];
        const reader = new FileReader();
        
        reader.addEventListener('load', function() {
            imageAvatar.src = reader.result;
        });
        reader.readAsDataURL(image);
    });

    let editPasswordButton = document.querySelector("#editPasswordButton")
    let modalWindowPassword = document.querySelector("#modalWindowPassword")
    let darkModal = document.querySelector("#darkModal")
    let closeButton = document.querySelector("#closeButton")

    editSavedPassword.addEventListener('click', ()=>{
        modalWindowPassword.classList.toggle("hidden-modal")
        darkModal.classList.toggle("hidden-modal")
        
    })

    closeButton.addEventListener('click', ()=>{
        modalWindowPassword.classList.toggle("hidden-modal")
        darkModal.classList.toggle("hidden-modal")
    })
    if (document.cookie.includes("add_verifictation_code")){
        modalWindowPassword.classList.toggle("hidden-modal")
        darkModal.classList.toggle("hidden-modal")
        editPassword.classList.toggle("hidden");
        passwordsDiv.classList.toggle("hidden");
        inputDivPassword.classList.toggle("hidden");
    }
})
