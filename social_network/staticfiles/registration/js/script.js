const eyeImages = document.querySelectorAll(".eye-img");


for (let count = 0; count < eyeImages.length; count++){
    let eyeImage = eyeImages[count];
    let input = document.getElementById(eyeImage.id)
    eyeImage.addEventListener("click", ()=>{
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
