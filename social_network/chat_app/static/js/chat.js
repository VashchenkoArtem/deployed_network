const chatGroup = document.getElementById("chatGroupId").value // Отримуємо value прихованого input з id групи.

const socketUrl = `wss://${window.location.host}/chats/all_chats/${chatGroup}`; //  Формуємо URL адресу для WS-з'єднання за поточним хостом

const socket = new WebSocket(socketUrl); // Ініціалізуємо WebSocket (Створюємо WS-з'єднання)

const messages = document.getElementById("messages"); // Отримуємо div з усіма повідомленнями.
const form = document.getElementById("form"); // Отримуємо об'єкт форми повідомлення.
const dateTime = document.querySelectorAll(".message-time"); // Отримуємо усі об'єкти дати та часу.
// Перебираємо усі об'єкти дати та часу.
for (let time of dateTime){
    let dateAndTime = new Date(time.textContent); // Створюємо об'єкт дати та часу, передаючи контент(дату та час) конкретного повідомлення.
    let dateAndTimeLocal = dateAndTime.toLocaleString([], { hour: '2-digit', minute: '2-digit' }); // Локалізуємо дату та час до годин | хвилин.
    time.textContent = dateAndTimeLocal // Передаємо контент зміненного повідомлення.
} 
// Перевіряємо відправку повідомлення.
form.addEventListener("submit", (event) => {
    // Відміняємо стандартну поведінку форми(відправки даних)
    event.preventDefault()
    // Отримуємо value повідомлення користувача.
    let message = document.getElementById("id_message").value
    // Створюємо JSONString та перетворюємо його в string | Відправляємо JSONString на сервер | Відправляємо на клієнт.
    socket.send(JSON.stringify({"message": message}))
    // Очищуємо messageForm без оновлення сторінки
    form.reset()
})


socket.addEventListener('message', function(event){ 
    const messageWithAvatar = document.createElement('div');
    
    const messageObject = JSON.parse(event.data);
    const messageElem = document.createElement('div');
    messageElem.classList.add("one-message");
    const username  = document.createElement('p');  
    const messageAndTime = document.createElement('div');
    const avatar = document.createElement('img');
    const hiddenInputId = document.querySelector(".input-name").value;
    if (Number(hiddenInputId) !== messageObject['user_id']){
        username.textContent = `${messageObject['username']}`;
        username.classList.add('message-author');
        messageElem.append(username);
        messageElem.classList.add("author-people");
        for (let count = 0; count < messageObject["all_avatars"].length; count ++){
            let ProfileAvatar = messageObject["all_avatars"][count]
            let profileId = messageObject["profile_id"]
            if (ProfileAvatar.fields.profile == profileId){
                avatar.classList.add("avatar-people");
                avatar.src = "/media/" + ProfileAvatar.fields.image
                messageWithAvatar.append(avatar)

            }
                else{
                    avatar.classList.add("avatar-people");
                    avatar.src = "/static/images/account.png"
                    messageWithAvatar.append(avatar)
                }
        messageWithAvatar.classList.add('message-with-avatar')
        messageWithAvatar.classList.add('author-people-message')
    }
    }
    else{ 
        messageElem.classList.add("author-me")
    }

    const message = document.createElement('p')
    message.textContent = `${messageObject['message']}`
    messageAndTime.append(message)
    const time = document.createElement('p')
    messageAndTime.classList.add("message-and-time")
    time.classList.add('message-time')
    let dateAndTime = new Date(messageObject['date_time']);
    let dateAndTimeLocal = dateAndTime.toLocaleString([], { hour: '2-digit', minute: '2-digit' });
    time.textContent = dateAndTimeLocal
    messageAndTime.append(time)

    message.classList.add("message-content")
    messageElem.append(messageAndTime)
    messageWithAvatar.append(messageElem)   
    messages.append(messageWithAvatar)
    scrollMessagesToBottom()
})

window.addEventListener('load', ()=>{
    let divMessages = document.querySelector('.messages-class')
    divMessages.scrollTop = divMessages.scrollHeight;
})

function scrollMessagesToBottom(){
    let divMessages = document.querySelector('.messages-class')
    divMessages.scrollTop = divMessages.scrollHeight;
}
