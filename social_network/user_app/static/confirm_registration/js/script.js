const Inputs = document.querySelectorAll(".input")

Inputs.forEach((input, index) => {
    input.addEventListener('input', () => {
        if (input.value.length === 1 && index < Inputs.length - 1){
            Inputs[index + 1].focus()
        }
    })
    input.addEventListener('keydown', (event) => {
        if (event.key === "Backspace" && input.value === "" && index > 0){
            Inputs[index - 1].focus()
        }
    })
})