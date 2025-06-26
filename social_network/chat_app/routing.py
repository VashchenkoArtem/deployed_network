'''
Файл для маршрутизації WebSocket запитів (аналог urls.py).
'''
from django.urls import path # Імпортуємо функцію path для створення маршрутів.
from .consumers import ChatConsumer # Імпортуємо клас, в якому прописана уся логіка WebSocket запитів.

# Створюємо список з url для обробки WebSocket-запитів.
ws_urlpatterns = [
    path("chats/all_chats/<int:chat_pk>", ChatConsumer.as_asgi(), name="chat") # Створємо шлях для chats, вказуючи ChatConsumer як асинхронний обробник для WebSocket запиту.
]