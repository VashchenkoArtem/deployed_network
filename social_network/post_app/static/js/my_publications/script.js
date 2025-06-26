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
const wrapperRedact = document.querySelectorAll(".redact-post")



postObject.addEventListener("click", function (event) {
    event.preventDefault();
    formObject.classList.toggle("hidden");
    bodyObject.classList.toggle("blur");
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
redactButtons.forEach((element, index) => {
    let formRedact = formsRedact[index];
    let wrapperObject = wrapperRedact[index];

    element.addEventListener("click", () => {
        formRedact.classList.toggle("hidden");
        bodyObject.classList.toggle("blur");
        wrapperObject.classList.toggle("hidden");

        $.ajax({
            url: `/check_info_post/${element.id}`,
            type: 'POST',
            data: {
                'pk': element.id,
                'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            success: function(response) {
                document.querySelectorAll("#field-title")[index].value = response.title;
                document.querySelectorAll("#field-topic")[index].value = response.topic;
                document.querySelectorAll("#field-text")[index].value = response.content;
                document.querySelectorAll("#field-url")[index].value = response.link;


            }
        });
    });
});



// Перебираємо усіх хрестиків для закриття модальних вікон
for (let count = 0; count < crossesRedact.length; count++) {
    let crossRedact = crossesRedact[count]; // Знаходимо один об'єкт хрестика по індексу count
    let formRedact = formsRedact[count]; //  Знаходимо об'єкт форми по індексу
    // Створюємо прослуховувач для кожного хрестика по кліку
    crossRedact.addEventListener("click", () => {
        formRedact.classList.toggle("hidden"); // Змінюємо клас hidden: якщо клас hidden заданий - видаляємо. Якщо класа немає - задаємо
        bodyObject.classList.toggle("blur"); // Змінюємо клас blur: якщо клас blur заданий - видаляємо. Якщо класа немає - задаємо
    });
}
const input = document.querySelector("#image-to-post-form"); // Знаходимо input по його айді
const previewDiv = document.querySelector("#image-preview-container"); // Знаходимо preview для картинок
// Якщо input з preview існує
if (input && previewDiv) {
    input.addEventListener("change", function () { // Створюємо прослуховувач по заданню картинок input
        previewDiv.innerHTML = ""; // Обнуляємо усі минулі картинки в input
        const files = Array.from(input.files); 
        // Перебираємо усі файли картинок в input. Кожен файл зберігається у змінній file
        files.forEach(file => { 
            // Перевіряємо, якщо тип файлу не починається на 'image/' - умова хибна
            if (!file.type.startsWith("image/")) return;
            const reader = new FileReader(); // Створюємо об'єкт для читання картинок
            // Загружаємо читача
            reader.onload = function (event) {
                const img = document.createElement("img"); // Створюємо елемент зображення
                img.src = event.target.result; // Отримуємо з читача результат та записуємо його до src зображення
                img.classList.add("post-images-form") // Задаємо клас зображенню для дизайну
                previewDiv.appendChild(img); // Записуємо елемент зображення до div-у
            };
            reader.readAsDataURL(file); // Записуємо результат читача як посилання
        });
    });
};

