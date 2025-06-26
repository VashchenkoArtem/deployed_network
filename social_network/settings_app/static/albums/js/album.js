let createAlbumButton = document.querySelector("#createAlbumButton")
let windowAddAlbum = document.querySelector("#windowAddAlbum")
let centerAddAlbum = document.querySelector("#centerAddAlbum")
let crossButton = document.querySelector("#crossButton")
let crossButtonRedact = document.getElementById("crossButtonRedact");
let cancelButtonRedact = document.getElementById("cancelButtonRedact")
let cancelButton = document.querySelector("#cancelButton")
let redactAlbumForm = document.getElementById('centerRedactAlbum');
let windowRedactAlbum = document.getElementById("windowRedactAlbum");
let dots = document.querySelectorAll(".dots");


createAlbumButton.addEventListener('click', ()=>{
    centerAddAlbum.classList.toggle('hidden')
    windowAddAlbum.classList.toggle('hidden')
})

crossButton.addEventListener('click', ()=>{
    centerAddAlbum.classList.toggle('hidden')
    windowAddAlbum.classList.toggle('hidden')
})
crossButtonRedact.addEventListener('click', ()=>{
    redactAlbumForm.classList.toggle('hidden');
    windowRedactAlbum.classList.toggle('hidden');
})
cancelButtonRedact.addEventListener('click', ()=>{
    redactAlbumForm.classList.toggle('hidden');
    windowRedactAlbum.classList.toggle('hidden');
})
cancelButton.addEventListener('click', ()=>{
    centerAddAlbum.classList.toggle('hidden')
    windowAddAlbum.classList.toggle('hidden')
})

for (let count = 0; count < dots.length; count ++){
    let dotsObject = dots[count];
    dotsObject.addEventListener("click", function(){
        redactAlbumForm.classList.toggle('hidden');
        windowRedactAlbum.classList.toggle("hidden");
    })
}
