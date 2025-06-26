"""
ASGI config for social_network project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
from chat_app.routing import ws_urlpatterns
from channels.auth import AuthMiddlewareStack


'''
os.environ.setdefault — встановлює змінну середовища, якщо вона ще не задана.

DJANGO_SETTINGS_MODULE — назва змінної, яка каже Django, який файл налаштувань використовувати.

'social_network.settings' — шлях до файлу з налаштуваннями.

'''
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network.settings')

# Створюємо змінну application (об'єкт додатку)
application = ProtocolTypeRouter({
    # При http-запиті викликається стандартна функція get_asgi_application(), яка перенаправить запит в urls.py
    'http': get_asgi_application(),
    # При ws-запиті викликається функція, яка відправить запит у routing.py
    'websocket': AuthMiddlewareStack(URLRouter(ws_urlpatterns)) 
})
