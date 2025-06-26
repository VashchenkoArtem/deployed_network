from django import forms # Імпортуємо модуль forms з django
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # Імпортужмо UserCreationForm та AuthenticationForm з django.contrib.auth.forms
from django.contrib.auth.models import User # Імпортуємо модель User з django.contrib.auth.models
from user_app.models import Profile # Імпортуємо модель Profile з settings_app.models


# Створюємо форму для реєстрації, яка наслідує UserCreationForm для створення нового користувача
class RegistrationForm(UserCreationForm):
    # Додаємо поле для введення електронної пошти
    email = forms.EmailField(max_length = 256,label = "Електронна пошта", widget = forms.EmailInput(attrs = {
                                                                        "placeholder": "you@example.com"
                                                                               })) #
    # Додаємо поле для введення імені користувача
    password1 = forms.CharField(max_length= 12,label = "Пароль", widget = forms.PasswordInput(attrs = {
                                                                        "placeholder": "Введи пароль"
                                                                                })) #
    # Додаємо поле для підтвердження пароля
    password2 = forms.CharField(max_length= 12,label = "Підтвердити", widget = forms.PasswordInput(attrs = {
                                                                        "placeholder": "Повтори пароль"
                                                                                })) #
    # Створюємо мета-клас для вказання моделі та полів, які будуть використовуватись у формі
    class Meta:
        model = User # Вказуємо модель, з якою працюватиме форма
        fields = ["email"] # Вказуємо поля, які будуть включені у форму
        
# Створюємо форму для авторизації, яка наслідує AuthenticationForm для входу користувача
class AuthorithationForm(forms.Form):
    # Додаємо поле для введення імені користувача або електронної пошти
    email = forms.EmailField(max_length= 256,label = "Пошта", widget=forms.EmailInput(attrs ={
        "placeholder": "you@example.com" # Задаемо плейсхолдер "you@example.com"
    })) 
    # Додаємо поле для введення пароля
    password = forms.CharField(widget = forms.PasswordInput(attrs = {
        "placeholder": "Введи пароль" # Задаемо плейсхолдер Введи пароль
    }), label = "Пароль") # Задаемо значення Лейбелу пароль


# Створюємо форму для верифікації, яка наслідує forms.Form для збору шести полів вводу
class VerificationForm(forms.Form):
    
    # Додаємо поле вводу 1 для верифікації
    input1 = forms.CharField(label = "", widget=forms.TextInput(attrs = { 
        "class": "input1 input", # Задаемо input1 input
        "inputmode": "numeric" #
    })) 
    # Додаємо поле вводу 2 для верифікації
    input2 = forms.CharField(label = "", widget=forms.TextInput(attrs = { #
        "class": "input2 input" #Задаемо input2 input
    })) 
    # Додаємо поле вводу 3 для верифікації
    input3 = forms.CharField(label = "", widget=forms.TextInput(attrs = { # 
        "class": "input3 input" #Задаемо input4 input
    }))
    # Додаємо поле вводу 4 для верифікації
    input4 = forms.CharField(label = "", widget=forms.TextInput(attrs = { #
        "class": "input4 input" #
    })) 
    
    # Додаємо поле вводу 5 для верифікації
    input5 = forms.CharField(label = "", widget=forms.TextInput(attrs = { #
        "class": "input5 input" # 
    })) 
    
    # Додаємо поле вводу 6 для верифікації
    input6 = forms.CharField(label = "", widget=forms.TextInput(attrs = { #
        "class": "input6 input" #
    })) 
    
    