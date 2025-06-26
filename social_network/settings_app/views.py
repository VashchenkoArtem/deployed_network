from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.urls import reverse_lazy
from user_app.models import Avatar, VerificationCode, Profile
from .forms import CreateAlbumForm
from post_app.models import Album, Image, Tag
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
import random


class UserSettingsView(TemplateView):
    template_name = 'user_settings/user_settings.html'
    def post(self, request, *args, **kwargs):
        response = redirect("user_settings")
        if not request.POST.get("hidden_input"):
            if request.POST.get("input1"):
                input1 = str(request.POST.get("input1"))
                input2 = str(request.POST.get("input2"))
                input3 = str(request.POST.get("input3"))
                input4 = str(request.POST.get("input4"))
                input5 = str(request.POST.get("input5"))
                input6 = str(request.POST.get("input6"))
                
                code_field = input1 + input2 + input3 + input4 + input5 + input6
                username = request.user.username
                user_code = VerificationCode.objects.get(username=username).code
                
                if user_code == code_field:
                    response.delete_cookie('add_verifictation_code')
                    VerificationCode.objects.get(username=username).delete()

            else:
                profile = Profile.objects.get(user_id = request.user.id)
                avatar = Avatar.objects.filter(profile = profile).first()
                new_name = request.POST.get('username')
                new_avatar = request.FILES.get('avatar')
                if new_avatar:
                    if avatar:
                        avatar.image = new_avatar
                        avatar.save()
                    else:
                        Avatar.objects.create(profile=profile, image=new_avatar)
                    return redirect("user_settings")
                if new_name :
                    if profile.user.username:
                        profile.user.username = new_name
                        profile.user.save()        
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