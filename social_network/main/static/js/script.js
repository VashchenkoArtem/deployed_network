const postObject = document.querySelector(".button-upload");
const formObject = document.querySelector(".frame-form");
const crossObject = document.querySelector(".cross");
const dotsList = document.querySelectorAll(".dots-post");
const dotsFormList = document.querySelectorAll(".dot-form");
const wrapperList = document.querySelectorAll(".redact-wrapper");
const bodyObject = document.querySelector(".full-screen");
const crossesRedact = document.querySelectorAll(".cross-redact");
const formsRedact = document.querySelectorAll(".redact-post-function");
const redactButtons = document.querySelectorAll(".redacting-title-redact");
const addTag = document.querySelector(".button-hashtag");
const inputPostMessage = document.querySelector(".post-message");
const fieldTitle = document.querySelectorAll("#field-title")


postObject.addEventListener("click", function (event) {
    event.preventDefault();
    formObject.classList.toggle("hidden");
    bodyObject.classList.toggle("blur");
    console.log(fieldTitle)
    fieldTitle[fieldTitle.length - 1].value = inputPostMessage.value
});
crossObject.addEventListener("click", function (event) {
    formObject.classList.toggle("hidden");
    bodyObject.classList.toggle("blur");
});
for (let count = 0; count < dotsList.length; count++) {
    let dotsObject = dotsList[count];
    let wrapperObject = wrapperList[count];
    dotsObject.addEventListener("click", function (event) {
        event.preventDefault();
        wrapperObject.classList.toggle("hidden");
    });
}
for (let count = 0; count < dotsFormList.length; count++) {
    let dotsObject = dotsFormList[count];
    let wrapperObject = wrapperList[count];
    dotsObject.addEventListener("click", function (event) {
        event.preventDefault();
        wrapperObject.classList.toggle("hidden");
    });
}
redactButtons.forEach(element => {
    let formRedact = formsRedact[element.id];
    let wrapperObject = wrapperList[element.id];
    element.addEventListener("click", () => {
        formRedact.classList.toggle("hidden");
        bodyObject.classList.toggle("blur");
        wrapperObject.classList.toggle("hidden");
        $.ajax({
            url: `post/check_info/${element.id}`,
            type: 'POST',
            data: {
                'pk': element.id,
                'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            success: function(response){
                let post = JSON.parse(response)[0]["fields"]
                document.querySelectorAll("#field-title")[element.id].value = post['title']
                document.querySelectorAll("#field-topic")[element.id].value = post['topic']
                document.querySelectorAll("#field-text")[element.id].value = post['text']
                document.querySelectorAll("#field-url")[element.id].value = post['url']
            }
        })
        
    });
})



for (let count = 0; count < crossesRedact.length; count++) {
    let crossRedact = crossesRedact[count];
    let formRedact = formsRedact[count];
    crossRedact.addEventListener("click", () => {
        formRedact.classList.toggle("hidden");
        bodyObject.classList.toggle("blur");
    });
}
const input = document.querySelector("#image-to-post-form");
const previewDiv = document.querySelector("#image-preview-container");
const customButton = document.querySelector("#custom-upload-button");

if (input && previewDiv && customButton) {
    customButton.addEventListener("click", function () {
        input.click();
    });

    input.addEventListener("change", function () {
        previewDiv.innerHTML = "";
        const files = Array.from(input.files);
        files.forEach(file => {
            if (!file.type.startsWith("image/")) return;
            const reader = new FileReader();
            reader.onload = function (event) {
                const img = document.createElement("img");
                img.src = event.target.result;
                img.classList.add("post-images-form");
                previewDiv.appendChild(img);
            };
            reader.readAsDataURL(file);
        });
    });
}


const addUrl = document.querySelector(".image-tag");

addUrl.addEventListener("click", function(){
    let cont = document.querySelector(".url-inputs");
    let lastInput = cont.querySelector(".input-url:last-child");
    let newInput = lastInput.cloneNode(true);

    let inputField = newInput.querySelector('input');
    if (inputField) {
        inputField.value = "";
    }
    cont.appendChild(newInput);
});

if (addTag){
    addTag.addEventListener('click', ()=>{
        document.querySelector(".add-tag").classList.toggle("hidden");
        document.querySelector(".image-confirm-tag").classList.toggle("hidden");
    })
}
// let tags = document.querySelectorAll(".tag-object")
// // if (tags){

//     // tags.forEach(tag => {
//     for (let count = 0;count < tags.length; count ++){
//         let tag = tags[count];
//         tag.addEventListener('click', ()=>{
//             // tag.style.backgroundColor = "rgb(194, 192, 196)"
//             // tag.style.color = "rgb(101, 84, 100)"
//             tag.classList.toggle("change-color") 
//         })
//     }
// }
document.querySelector('.tag-container').addEventListener('click', function(element){
    if (element.target.classList.contains('tag-object')) {
        element.target.classList.toggle("change-color");
    }
})