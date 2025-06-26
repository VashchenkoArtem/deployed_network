from django.contrib.auth.models import User # Імпортуємо модель User
from django.contrib.auth.backends import ModelBackend # Імпортуємо звичайні налаштування backend

# Створюємо клас особливого налаштування backend
class LoginEmail(ModelBackend):
    # Перестворюємо функцію authenticate
    def authenticate(self, request, username = None, password = None, **kwargs):
        try: # Створюємо оператор try-except
            user = User.objects.get(email=username) # Знаходимо користувача не по ім'ю, а по пошті
            if user.check_password(password): # Перевіряємо пароль
                return user # Повертаємо користувача 
        except User.DoesNotExist: # Якщо юзер не знайдений 
            return None # Повертаємо None