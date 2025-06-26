from django.views.generic.edit import CreateView, FormView # Імпортуємо класи відображення для створення власних.
from django.views.generic import TemplateView # Імпортуємо клас відображення для створення та рендерінгу власного.
from django.urls import reverse_lazy # Імпортуємо reverse_lazy для надання зворотного URL як атрибут url загального відображення на основі класу.
from .forms import VerificationForm, AuthorithationForm, RegistrationForm # Імпортуємо створені форми для валідації даних.
from django.core.mail import send_mail # Імпортуємо функцію send_mail для відправки gmail-листа користувачеві.
import random # Імпортуємо random для створення шестизначного коду.
from django.contrib.auth.models import User # Імпортуємо модель User для створення користувача.
from user_app.models import VerificationCode # Імпортуємо створені моделі профілю та верифікації.
from django.contrib.auth import authenticate, login # Імпортуємо функцію authenticate | login для аутентифікації та логіну користувача.
from django.shortcuts import redirect #
from user_app.models import Profile
from datetime import date


# Створюємо клас RegistrationView на базі вже створенного CreateView для відображення та логіки сторінки реєстрації.
class RegistrationView(CreateView):
    form_class = RegistrationForm # Вказуємо форму для роботи з валідними даними.
    template_name = "registration/index.html" # Вказуємо файл html для відображення сторінки.
    success_url = reverse_lazy("confirm") # Вказуємо подію перекиду на сторінку верифікації після успішної реєстрації користувача.

    # Створюємо функцію post для .
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email') # Отримуємо email, який користувач відправив у формі при реєстрації.
        if not User.objects.filter(email = email).exists(): # Якщо користувача з такою поштою ще нема.
            return super().post(request, *args, **kwargs) # Успадковуємо батьківський метод post, щоб продовжити стандартну обробку запиту.
        else:
            return redirect("registration") # Або перекидаємо користувача на сторінку реєстрації.
        
    # Створюємо метод form_valid, який відпрацює після того, як дані у формі будуть валідовані.
    def form_valid(self, form):
        response = super().form_valid(form) # Успадковуємо батьківський метод form_valid.
        response.set_cookie('email', form.cleaned_data['email'], max_age=3600) # Записуємо у cookie валідований email користувача на годину.
        special_code = random.randint(99999, 999999) # Створюємо рандомний шестизначний код для підтвердження особистості.
        # user_id = User.objects.get(email = form.cleaned_data['email']).id 
        user = form.save() # Зберігаємо у базу даних дані із форми.
        user.username = f"user-{user.pk}" # Додаємо вручну поле username з його id, яке є обов'язковим для бази даних і необов'язковим для реєстрації користувача.
        user.save() # Зберігаємо у базу даних створений username.
        Profile.objects.create(user = user, date_of_birth = date.today()) # Створюємо профіль на основі даних.
        VerificationCode.objects.create(username = user.username, code = special_code) # Створюємо та зберігаємо у базу даних шестизначний код.
        # Відправляємо email.
        send_mail(
            subject = "Код для підтвердження", # Заголовок листа.
            message = f"Вітаємо!\n ваш код для підтвердження: {special_code}", # Контент листа.
            from_email = "qrprojectdjangoteam2@gmail.com", # Email проєкту, від лиця якого надсилається лист.
            recipient_list = [f"{form.cleaned_data['email']}"], # Відправляємо на адресу користувача.
            fail_silently = False # Якщо в процесі відправки листа відбудеться помилка, показати її.
            )
        # Повертаємо response.
        return response
# Створюємо клас ConfirmRegistrationView для відображення сторінки та логіки на сторінці confirm. 
class ConfirmRegistrationView(FormView):
    template_name = "registration_confirm/index.html" # Вказуємо файл html для відображення сторінки.
    form_class = VerificationForm # Вказуємо форму для роботи з валідними даними.
    success_url = reverse_lazy("authorithation") # Вказуємо подію перекиду на сторінку аутентифікації після успішної реєстрації користувача.

    # Створюємо метод form_valid, який відпрацює після того, як дані у формі будуть валідовані.
    def form_valid(self, form):
        '''
            Отримуємо з форми маленькі валідовані інпути для введення даних.
        '''
        input1 = str(form.cleaned_data["input1"])
        input2 = str(form.cleaned_data["input2"])
        input3 = str(form.cleaned_data["input3"])
        input4 = str(form.cleaned_data["input4"])
        input5 = str(form.cleaned_data["input5"])
        input6 = str(form.cleaned_data["input6"])
        
        code_field = input1 + input2 + input3 + input4 + input5 + input6 # Створюємо код на основі інпутів. 
        email= self.request.COOKIES.get("email") # Отримуємо з cookie email користувача.
        username = User.objects.get(email = email).username # Отримуємо з бази даних користувача з email, на який було відправлено лист.
        user_code = VerificationCode.objects.get(username = username).code # Отримуємо з бази даних користувача з тільки-що надісланним кодом.
        
        if user_code == code_field: # Якщо код, який ввів користувач, правильний ш збігається з тим, що надісланий у листі.
            VerificationCode.objects.get(username = username).delete() # Видаляємо код з бази даних.
            return super().form_valid(form) # Повертаємо батьківський form_valid.
        else:
            form.add_error(None, "Код підтвердження не підходе!") # Якщо ні, виводити помилку.
            return self.form_invalid(form) # Форма не валідна.

# Створюємо клас AuthorizationView для відображення сторінки та логіки на сторінці authorization. 
class AuthorizationView(FormView):
    template_name="authorization/index.html" # Вказуємо файл html для відображення сторінки.
    form_class = AuthorithationForm # Вказуємо форму для роботи з валідними даними.
    success_url = "/" # Перекид на головну сторінку після успішної аутентифікації.

    # Створюємо метод form_valid, який відпрацює після того, як дані у формі будуть валідовані.
    def form_valid(self, form):
        email = form.cleaned_data['email'] # Отримуємо з форми введений email користувача.
        password = form.cleaned_data['password'] # Отримуємо з форми введений password користувача.
        # Перевіряємо, чи існує користувач з таким username та password.
        user = authenticate(username = email, password = password)
        # Якщо існує, то 
        if user is not None:
            login(self.request, user) # Логінемо користувача
            return super().form_valid(form) # Повертаємо батьківський form_valid.
        else:
            form.add_error(None, "Невірна пошта або пароль") # Якщо ні, виводити помилку.
            return self.form_invalid(form) # Форма не валідна.