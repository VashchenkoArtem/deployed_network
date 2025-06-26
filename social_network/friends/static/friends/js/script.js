// $(document).ready(function(){  // 
//     $(".button-delete").each(function(){  //  Кнопка видалення 
//         $(this).on('click', function(){  //  Оброблюємо по натисканню клавіши
//             let url = $(this)  // 
//             $.ajax({  // Оброблюємо ajax
//                 url: url.attr('id'),  // Значення айди як Юрл запиту
//                 type: "get", // Метод запроса-GET,отримання
//                 success: function(){  //  Успішне виконання 
//                     let userId = url.attr('id').split("/")[3]; // 
//                     console.log(userId) // Відоброжаємо айди у консоль
//                     if ($(`#card-request-${userId}`)){  // 
//                         let card = $(`#card-request-${userId}`);  // Отримуемо елемент
//                         card.toggleClass("hidden");  // Задаемо значення карточки, скритне
//                     }
//                 }
//             })
//         })
//     })


$(document).ready(function(){  // Якщо документ готовий(завантажився).
    $(".button-delete").each(function(){  // Отримуємо усі об'єкти кнопки видалення та перебираємо їх.
        $(this).on('click', function(){  //  Оброблюємо натиск на конкретну кнопку.
            let url = $(this)  // Створюємо та записуємо в змінну url конкретну кнопку.
            $.ajax({  // Формуємо AJAX запит.
                url: url.attr('id'),  // В url передаємо як значення id конкретної кнопки, щоб відправляти по ній запит.
                type: "get", // Метод запиту - get.
                success: function(){  //  Успішне виконання 
                    let userId = url.attr('id').split("/")[3]; // Отримуємо значення id у конкретної кнопки. Розбиваємо та ділимо рядок, вилучаємо елемент з індексом 3(id користувача).
                    // console.log(userId)

                    if ($(`#card-request-${userId}`)){  // Шукаємо картку з конкретним id, яку потрібно видалити. 
                        let card = $(`#card-request-${userId}`);  // Записуємо знайденну картку у змінну для зручності.
                        card.toggleClass("hidden");  // Змінюємо клас елементу(Приховуємо від користувача при натисканні "Видалити").
                    }
                }
            })
        })
    })



    $(".button-delete-recommended").each(function(){ // Кнока видалення рекомендацій
        $(this).on('click', function(){ // Оброблюємо натискання по клавіши
            let url = $(this) // 
            $.ajax({ // Оброблюємо ajax
                url: url.attr('id'), // Значення айди як Юрл запиту
                type: "get", // Метод запроса-GET,отримання
                success: function(){ // Успішне виконання 
                    let userId = url.attr('id').split("/")[3]; //
                    console.log(userId) // Відображуемо айди у консоль 
                    if ($(`#card-recommended-${userId}`)){ //
                        let card = $(`#card-recommended-${userId}`); // Отримуемо елемент
                        card.toggleClass("hidden"); //  Задаемо значення карточки, скритне
                    }
                }
            })
        })
    })
    $(".button-delete-friend").each(function(){ // Кнопка видалення друзів
        $(this).on('click', function(){ //  Оброблюємо натискання по клавіши 
            let url = $(this) // 
            $.ajax({ // Оброблюємо ajax
                url: url.attr('id'), //Значення айди як Юрл запиту
                type: "get", // Метод запроса-GET,отримання
                success: function(){ // Успішне виконання 
                    let userId = url.attr('id').split("/")[3]; //
                    console.log(userId) // Відображуемо айди юзера  у консоль 
                    if ($(`#card-friend-${userId}`)){ //
                        let card = $(`#card-friend-${userId}`); // 
                        console.log(card) // Відображуемо карточку у консоль
                        card.toggleClass("hidden");  //  Задаемо значення карточки, скритне
                    }
                }
            })
        })
    })
    $(".add-button").each(function(){ // Додаемо кнопку
        $(this).on('click', function(){ //  Оброблюємо натискання по клавіши 
            let url = $(this) //
            $.ajax({ //  Оброблюємо ajax
                url: url.attr('id'), // Значення айди як Юрл запиту
                type: "get", // Метод запроса-GET,отримання
                success: function(){ //  Успішне виконання 
                    $(".confirm-delete-div").toggleClass('hidden') // Підтвердження видалення задаємо значення скритне 
                }
            })
        })
    })
    $(".button-confirm-recomended").each(function(){ // Кнопка підтвердити рекомендації
        $(this).on('click', function(){ // Оброблюємо натискання по клавіши 
            let url = $(this) // 
            $.ajax({ // Оброблюємо ajax
                url: url.attr('id'), // Значення айди як Юрл запиту
                type: "get", //  Метод запроса-GET,отримання
                success: function(){ // Успішне виконання 
                    let userId = url.attr('id').split("/")[3]; //
                    console.log(userId) // Відображуемо айди юзера у консоль
                    if ($(`#card-recommended-${userId}`)){ //
                        let card = $(`#card-recommended-${userId}`); //
                        card.toggleClass("hidden"); // Задаемо значення скритне
                    }
                }
            })
        })
    })
    $(".icon-like").each(function(element){ //  
        $(this).on('click', function(){ // Оброблюємо натискання по клавіши 
            let id = this.id; // Задаемо значення айди як  теперішнє айди
            let classObject = $(this).attr("class").split(' ')[2] /
            console.log(classObject) // Відображуемо у консоль classObject
            $.ajax({ //Оброблюємо ajax
                url: id, // Значення юрл як айди
                type: "get", //Метод запроса-GET,отримання
                success: function(){ //Успішне виконання 
                    let likes = $(`#likesPost-${classObject}`); // Оброблюемо лайки поста
                    let updatedLikes = Number(likes.text()) + 1 // Оброблюемо оновлення лайків
                    likes.text(updatedLikes) // Теперешнє значення лайків яке оновлюеться завдяки методу оновлення лайків
                }
            })
        })
    });
})
