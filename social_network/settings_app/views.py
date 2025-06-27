from django.shortcuts import render, redirect # Імпортуємо функції для відображення сторінки або для переходу на іншу
from django.views.generic import TemplateView, View # Імпортуємо необхідні класи відображення
from django.views.generic.edit import UpdateView, CreateView # Імпортуємо необхідні класи відображення
from django.contrib.auth.models import User # Імпортуємо готову модель користувача
from django.urls import reverse_lazy # Імпортуємо параметр, який формує посилання до сторінки за допомогою імені
from user_app.models import Avatar, VerificationCode, Profile # Імпортуємо особисті моделі: Аватара, кода підтвердження та профіля
from .forms import CreateAlbumForm # Імпортуємо форму створення альбомів
from post_app.models import Album, Image, Tag # Імпортуємо моделі альбома, зображення та тега
from django.contrib.auth import update_session_auth_hash # Імпортуємо функцію, яка допомогає оновити хеш авторизації
from django.core.mail import send_mail # Імпортуємо функцію відправки повідомлення на пошту
import random # Імпортуємо бібліотеку, який дозволяє генерувати випадкові числа
from django.db import IntegrityError # Імпортуємо помилку, щоб відловитти її нижче


# Клас відображення для налаштувань даних користувача
class UserSettingsView(TemplateView):
    template_name = 'user_settings/user_settings.html' # Задаємо шлях до template шаблона
    # Метод post, завдяки якому можемо зрозуміти коли відбувається відправка форм
    def post(self, request, *args, **kwargs): 
        response = redirect("user_settings") # Об'єкт запита
        if not request.POST.get("hidden_input"): # Якщо форма немає input з іменем hidden_input
            if request.POST.get("input1"): # Якщо форма має input з іменем input1
                input1 = str(request.POST.get("input1")) # Знаходимо введені дані з input з іменем input1-input6
                input2 = str(request.POST.get("input2"))
                input3 = str(request.POST.get("input3"))
                input4 = str(request.POST.get("input4"))
                input5 = str(request.POST.get("input5"))
                input6 = str(request.POST.get("input6"))
                code_field = input1 + input2 + input3 + input4 + input5 + input6 # Беручи усі input ми дізнаємося код підтверждення, який ввів користувач
                username = request.user.username # Дізнаємося ім'я користувача
                user_code = VerificationCode.objects.get(username=username).code # Дізнаємося код підтверждення користувача 
                
                if user_code == code_field: # Якщо код, який ввів користувач співпадає з кодом з БД
                    response.delete_cookie('add_verifictation_code') # Видаляємо з cookie рядок add_verification_code
                    VerificationCode.objects.get(username=username).delete() # Видаляємо об'єкт кода підтвердження користувача
            else: # Інакше
                profile = Profile.objects.get(user_id = request.user.id) # Беремо профіль користувача
                avatar = Avatar.objects.filter(profile = profile).first() # Беремо аватарки користувача
                new_name = request.POST.get('username') # Дізнаємося значення input нового ім'я користувача, який ввів користувач
                new_avatar = request.FILES.get('avatar') # Дізнаємося значення input нового аватара користувача, який ввів користувач
                if new_avatar: # Якщо поле нового аватара було заповнене
                    if avatar: # Якщо існує старий аватар
                        avatar.image = new_avatar # Змінюємо картинку старого аватара на нову
                        avatar.save() # Зберігаємо зміни в БД
                    else: # Інакше
                        Avatar.objects.create(profile=profile, image=new_avatar) # Створюємо об'єкт аватара
                    return redirect("user_settings") # Перекидаємо користувача на сторінку налаштування
                if new_name: # Якщо поле нове ім'я було заповнене
                    try:
                        if profile.user.username:
                            profile.user.username = new_name
                            profile.user.save()    
                    except IntegrityError:
                        print("Error")
                        return render(request, self.template_name, context = {"error_name": "Користувач з таким іменем вже існує!"})
                return redirect("user_settings")
        elif request.POST.get("hidden_input"):
            username = request.user.username
            special_code = random.randint(99999, 999999)
            VerificationCode.objects.create(username = request.user.username, code = special_code)
            send_mail(
                subject = "Код для підтвердження",
                message = f"Вітаємо!\n ваш код для підтвердження зміни паролю: {special_code}",
                from_email = "qrprojectdjangoteam2@gmail.com",
                recipient_list = [f"{request.user.email}"],
                fail_silently = False
            )
            user = User.objects.get(username=username)
            password1 = request.POST.get("password")
            password2 = request.POST.get("confirm_password")
            if password1 == password2:
                user.set_password(password1)
                user.save()
                update_session_auth_hash(request, user)
                response.set_cookie('add_verifictation_code', "True")
                return response
            return response
        return response

    def get_context_data(self, **kwargs):
        context = super(UserSettingsView, self).get_context_data(**kwargs)
        profile = Profile.objects.get(user_id = self.request.user.id)
        context['my_avatar'] = Avatar.objects.filter(profile = profile, shown = True, active = True).first()
        return context
    def dispatch(self, request, *args, **kwargs):
        if not Profile.objects.filter(user_id = request.user.id).exists():
            return redirect("registration")
        else:   
            return super().dispatch(request, *args, **kwargs)

class UserAlbums(CreateView):
    template_name = 'albums/albums.html'
    form_class = CreateAlbumForm
    success_url = reverse_lazy('albums')
    def get_context_data(self, **kwargs):
        context = super(UserAlbums, self).get_context_data(**kwargs)
        profile = Profile.objects.get(user_id = self.request.user.id)
        context['all_albums'] =  Album.objects.filter(author = profile)
        context['my_avatars'] = Avatar.objects.filter(profile = profile, shown = True, active = True)
        context['all_tags'] = Tag.objects.all()
        try:
            context['album_photos'] = Album.objects.all().first().images.all()
        except:
            print("error")
        return context
    def post(self, request, *args, **kwargs):
        if request.POST.get('album_pk'):
            albums_photos = request.FILES.getlist('photos')
            album_pk = request.POST.get('album_pk')
            album = Album.objects.get(id = album_pk)
            for photo in albums_photos:
                picture = Image.objects.create(filename = photo.name, file = photo)
                album.images.add(picture)
        return super().post(request, *args, **kwargs)
    def dispatch(self, request, *args, **kwargs):
        if not Profile.objects.filter(user_id = request.user.id).exists():
            return redirect("registration")
        else:   
            return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        album = form.save(commit=False)
        album.author_id = Profile.objects.get(user_id = self.request.user.id).id
        album.save()
        return super().form_valid(form)
class FriendsView(TemplateView):
    template_name = "friends/friends.html"

class RedactDataView(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'user_settings/user_settings.html'
    success_url = reverse_lazy('user_settings')

    def get_object(self, queryset=None):
        return self.request.user

class RedactAlbumView(UpdateView):
    model = Album
    fields = ['name', 'topic']
    template_name = "albums/albums.html"    
    success_url = reverse_lazy('albums')

class ChangePasswordView(View):
    def post(self, request, *args, **kwargs):
        # user = request.user              
        # password1 = request.POST.get("password")
        # password2 = request.POST.get("confirm_password")
        # if password1 == password2:      
        #     user.set_password(password1)
        #     user.save()                 
        #     update_session_auth_hash(request,user)
        return redirect("user_settings") 