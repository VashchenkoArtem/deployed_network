const buttonCreateGroup = document.querySelector('.add-chat');
const formObject = document.querySelector(".modal-create-group-create");
const frameCross = document.querySelector(".close-create-group-name");
const fullscreen = document.querySelector(".fullscreen");
const groupModal = document.querySelector(".modal-set-name");
const buttonCreate = document.querySelector(".confirm-create-group");
const inputImage = document.getElementById("add-image-avatar");
const imageAvatar = document.querySelector(".group-image");
const editFormName = document.querySelector(".edit-form-name");
const dots = document.querySelectorAll(".dots");
const addMemberButton = document.querySelector(".add-member-button");
const editFormMembers = document.querySelector(".modal-edit-group");
const editGroup = document.querySelector(".confirm-create-group");
const crossImage = document.querySelectorAll(".close-second-modal");
const editName = document.querySelector(".modal-edit-name")
const modalInfo = document.querySelector('.modal-info');
const buttonEditGroup = document.querySelector('.edit-group');
const closeEditUsers = document.querySelector('.close-redact-users');
const closeEditGroup = document.querySelector('.close-redact-group');


buttonCreateGroup.addEventListener("click", ()=>{
    formObject.classList.toggle("hidden");
    fullscreen.classList.toggle("hidden");
})
frameCross.addEventListener("click", ()=>{
    formObject.classList.toggle("hidden");
    fullscreen.classList.toggle("hidden");
})
const cookies = document.cookie.split(';')
for (let cookieField of cookies){
    if (cookieField.includes("group_members")){
        if (editName){
            fullscreen.classList.toggle("hidden");
            editName.classList.toggle("hidden");
        }
        else{   
            fullscreen.classList.toggle("hidden");
            groupModal.classList.toggle("hidden");
        }
    }
}
inputImage.addEventListener('change', function(){
    let image = inputImage.files[0];
    let reader = new FileReader();
    reader.addEventListener('load', function(){
        imageAvatar.src = reader.result;
    })
    reader.readAsDataURL(image);
})
if (dots){
    for (let count = 0; count < dots.length; count ++){
        let oneObjectDots = dots[count];
        oneObjectDots.addEventListener('click', function(){
            modalInfo.classList.toggle("hidden");
        })
    }


}
if (addMemberButton){
    addMemberButton.addEventListener('click', function(){
        editFormName.classList.toggle("hidden");
        editFormMembers.classList.toggle("hidden");
})
}

for (let field of cookies){
    if (field.includes("get_friends")){
        editFormName.classList.toggle('hidden');
    }
}
if (crossImage){
    for (let count = 0; count < crossImage.length; count++){
        let oneCrossImage = crossImage[count];
        oneCrossImage.addEventListener("click", function(){
            groupModal.classList.toggle('hidden');
            fullscreen.classList.toggle("hidden");
            document.cookie = "group_members=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        })
    }
}

if (buttonEditGroup){
    buttonEditGroup.addEventListener("click", function(){
        editName.classList.toggle('hidden');
        fullscreen.classList.toggle("hidden");
    })
}

if (closeEditGroup){
    closeEditGroup.addEventListener('click', function(){
        editName.classList.toggle('hidden');
        fullscreen.classList.toggle("hidden");
    })
}
if (closeEditUsers){
    closeEditUsers.addEventListener('click', function(){
        editFormMembers.classList.toggle('hidden');
        fullscreen.classList.toggle("hidden");

    })
}