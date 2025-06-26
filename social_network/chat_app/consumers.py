from channels.generic.websocket import AsyncWebsocketConsumer # Імпортуємо AsyncWebsocketConsumer - клас у Django Channels, який дозволяє створювати асинхронні WebSocket-з'єднання між сервером і браузером у реальному часі.
import json # Імпортуємо json для майбутньої передачі text_data у javascript.
from .forms import MessageForm # Імпортуємо форму для відправки валідованих повідомленнь.
from channels.db import database_sync_to_async, sync_to_async # Імпортуємо декоратор database_sync_to_async для асинхронної роботи бази даних та декоратор sync_to_async для створення асинхронних методів.
from .models import ChatGroup, ChatMessage # Імпортуємо моделі для роботи з кімнатами чатів та для повідомлень.
from user_app.models import Profile, Avatar # Імпортуємо моделі для роботи з користувачем.
from django.core import serializers # Імпортуємо модуль serializers, щоб використовувати функцію serialize для форматування python-рядка у json-рядок.

# Створили клас ChatConsumer, який відповідає за з'єднання сервера с клієнтом. Він відловлює запити та обробляє їх.
class ChatConsumer(AsyncWebsocketConsumer):
    # Створюємо асинхронний метод connect, який відпрацьовує після запиту про підключення.
    async def connect(self):
        self.chat_pk = str(self.scope["url_route"]["kwargs"]["chat_pk"]) # Отримуємо id групи з динамічного поточного URL під ім'ям "chat_pk".
        self.group_name = self.chat_pk # Створюємо назву поточному чату.

        # Під'єднуємо поточного користувача (тобто його канал) до групи, котра вказана в динамічному URL.
        await self.channel_layer.group_add(
            self.group_name, self.channel_name
        )

        # Запит про підключення схвалений.
        await self.accept()

    # Створюємо асинхронний метод receive, який відпрацьовує коли сервер отримує повідомленя від клієнта.
    async def receive(self, text_data):
        self.user = self.scope["user"] # Отримуємо поточного користувача.
        username = self.user.username # Отримуємо ім'я поточного користувача.
        id = self.user.id # Отримуємо id поточного користувача.
        avatars = await self.get_avatars() # Викликаємо асинхрону функцію get_avatars для отримання всіх аватарів.
        profile = await self.get_profile() # Викликаємо асинхрону функцію get_profile для отримання всії профілів.
        saved_message = await self.save_message(message = json.loads(text_data)['message']) # Зберігаеємо повідомлення у базу даних та у змінну "saved_message".
        # Відправляємо повідомлення всім участникам групи.
        await self.channel_layer.group_send(self.group_name,
            {
                "type": "send_message_to_chat", # Вказуємо тип обробника (метод, що викличиться для відправки повідомлення).
                "text_data": text_data, # Передаємо повідомлення користувача через event, send_message_to_chat.
                "username": username, # Передаємо користувача(автора повідомлення).
                "date_time": saved_message.sent_at, # Передаємо час відправки повідомлення.
                "user_id": id, # Передаємо id поточного користувача.
                "all_avatars": avatars, # Передаємо аватар користувача.
                "profile_id":profile # Передаємо профіль користувача.
            })
        
    # Створюємо асинхронний метод відправки повідомлення до чату.
    async def send_message_to_chat(self, event):
        text_data_dict = json.loads(event['text_data']) # Перетворюємо текст з формату json у python словник.
        form = MessageForm(text_data_dict) # Передаємо дані у форму для валідації
        username = event['username'] # Отримуємо username поточного користувача
        text_data_dict['username'] = username # Записуємо ім'я поточного користувача до словника у форматі json, щоб отримати та використати у js.
        '''
        Записуємо дату та час відправлення повідомлення до словника у форматі json, 
        щоб отримати та використати у js. Використовуємо функцію isoformat() для переведення дати у iso-формат, 
        щоб локалізувати час у файлі chat.js
        '''
        text_data_dict['date_time'] = event['date_time'].isoformat()
        text_data_dict['user_id'] = event['user_id'] # Записуємо id поточного користувача до словника у форматі json, щоб отримати та використати у js.
        text_data_dict['profile_id'] = event['profile_id'] # Записуємо профіль поточного користувача до словника у форматі json, щоб отримати та використати у js.
        
        if form.is_valid(): # Якщо форма валідна(повідомлення проходить валідацію).
            await self.send(json.dumps(text_data_dict)) # Відправляємо повідомлення користувачу у форматі json для роботи у chat.js.
    
    # Використовуємо декоратор database_sync_to_async для асинхронної роботи бази даних.
    @database_sync_to_async
    # Створюємо функцію для збереження повідомлення.
    def save_message(self, message):
        content = message # Передаємо контент повідомлення.
        author = Profile.objects.get(user = self.scope["user"]) # Передаємо автора поточного повідомлення.
        group = ChatGroup.objects.get(pk = self.group_name) # Отримуємо поточну групу, у яку потрібно зберігати повідомлення.
        return ChatMessage.objects.create(content = content, author = author, chat_group = group) # Повертаємо створене повідомлення
    
    # Використовуємо декоратор sync_to_async для створення асинхронних методів.
    @sync_to_async
    # Створюємо метод, який потрібен для отримання усіх аватарів.
    def get_avatars(self):
        all_avatars = Avatar.objects.all() # Отримуємо всі аватари.
        return json.loads(serializers.serialize("json", all_avatars)) # Перероблюємо та повертаємо отриманні дані у json-формат для роботи із chat.js.
    
    # Використовуємо декоратор sync_to_async для створення асинхронних методів.
    @sync_to_async
    # Створюємо метод, який потрібен для отримання усіх профілів.
    def get_profile(self):
        self.user = self.scope["user"] # Отримуємо поточного користувача.
        id = self.user.id # Отримуємо id користувача
        profile_id = Profile.objects.get(user_id = id) # Отримуємо усі профілі.
        return profile_id.id # Повертаємо id усіх профілів.