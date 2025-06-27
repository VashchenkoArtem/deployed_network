from django.views.generic.edit import CreateView, DeleteView, UpdateView # Імпортуємо класи для створення, видалення та редагування об'єктів
from django.views.generic import View # Імпортуємо клас для створення власних представлень
from .forms import PostForm # Імпортуємо форму для створення постів
from post_app.models import Post,Image, Tag, Link # Імпортуємо моделі для роботи з публікаціями
from .forms import PostForm, PostFormEdit # Імпортуємо форми для створення та редагування постів
from user_app.models import Friendship, Avatar, Profile # Імпортуємо моделі профілю, дружби та аватарів
from django.urls import reverse_lazy # Імпортуємо функцію для отримання URL-адреси за назвою
from django.contrib.auth.views import LogoutView # Імпортуємо клас для виходу з системи
from django.shortcuts import redirect # Імпортуємо функцію для перенаправлення користувача на іншу сторінку
from django.http import JsonResponse #Імпортуємо клас для створення JSON-відповідей
from django.core import serializers # Імпортуємо модуль для серіалізації об'єктів
from django.contrib.auth.models import User # Імпортуємо модель користувача
from .forms import UserUpdateForm # Імпортуємо форму для оновлення користувача
from chat_app.models import ChatGroup # Імпортуємо модель групи чату


# Створюємо представлення для головної сторінки, де користувач може створювати та переглянути пости.
class MainView(CreateView):
    template_name = "main/index.html" # Вказуємо шаблон для головної сторінки
    form_class = PostForm # Вказуємо форму для створення постів
    success_url = "/" #
    #
    def form_valid(self, form): 
        profile = Profile.objects.get(user_id=self.request.user.pk) #
        form.instance.author = profile #
        response = super().form_valid(form) #
        urls = self.request.POST.getlist('url')   #
        for url in urls: #
            url = Link.objects.create(post = self.object, url = url) #
        
        files = self.request.FILES.getlist('images') #
        for file in files: #
            image = Image.objects.create(filename = f"photo-{self.object}", file=file) #
            self.object.images.add(image) #
        return response #
    #
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if not Profile.objects.filter(user_id = request.user.id).exists(): # 
            return redirect("registration") #
        # current_user = Profile.objects.get(user_id = self.request.user.pk) #
        # user_posts = Post.objects.all() #
        # if len(user_posts) > 0: #
        #     for post_view in user_posts: #
        #         post_view.views.add(current_user) #
        #         post_view.save() #
        response.set_cookie("user_id", request.user.id)
        return response #
    #
    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs) #
        context["posts"] = Post.objects.order_by('-id')[:3] # 
        # context["tags"] = Tag.objects.all() # 
        # context['people'] = Profile.objects.get(user_id = self.request.user.pk) #
        # profile_id = self.request.COOKIES['current_profile_id']
        # context["all_urls"] = Link.objects.none() 
        # profile = Profile.objects.get(user_id = self.request.user.pk) # 
        # context["posts_count"] = Post.objects.filter(author_id = profile_id) # 
        # context["my_friends"] = Friendship.objects.filter(profile2 = profile, accepted = True) #
        # context["all_requests"] = Friendship.objects.filter(profile2 = profile) #
        # context["all_users"] = Profile.objects.none() #
        # context["users"] = User.objects.none() 
        author_avatars = {} #
        # for author in Profile.objects.filter(id__in=Post.objects.values_list('author_id', flat=True)): #
        #     avatar = Avatar.objects.filter(profile=author, shown=True, active=True).first() #
        #     author_avatars[author.id] = avatar #
        # for group in ChatGroup.objects.all(): #
        #     for member in group.members.all(): #
        #         if member.id not in author_avatars: #
        #             avatar = Avatar.objects.filter(profile=member, shown=True, active=True).first() #
        #             author_avatars[member.id] = avatar #
        # for friend_ship in Friendship.objects.all(): #
        #     if friend_ship.profile1 == Profile.objects.get(user_id = self.request.user.pk): #
        #         if friend_ship.profile2.id not in author_avatars: #
        #             avatar = Avatar.objects.filter(profile=friend_ship.profile2, shown=True, active=True).first()#
        #             author_avatars[friend_ship.profile2.id] = avatar #
        #     if friend_ship.profile2 == Profile.objects.get(user_id = self.request.user.pk): #
        #         if friend_ship.profile1.id not in author_avatars: #
        #             avatar = Avatar.objects.filter(profile=friend_ship.profile1, shown=True, active=True).first() #
        #             author_avatars[friend_ship.profile1.id] = avatar #


        context['author_avatars'] = author_avatars 
        # context["my_avatars"] = Avatar.objects.filter(profile_id = context["profile_id"]).first() #
        context['all_groups'] = ChatGroup.objects.none() #
        # context["current_user"] = profile #
        context['all_views'] = Post.objects.none() #
        # for post in Post.objects.filter(author_id = context["profile_id"]): #  
        #     context['all_views'] = context['all_views'] | post.views.order_by("-id")[:3] #
        # context["tags"] = Tag.objects.all() # 
        # context['people'] = Profile.objects.get(user_id = self.request.user.pk) #
        # context["all_urls"] = Link.objects.all() 
        # context['all_peoples'] = Profile.objects.all() #
        # profile = Profile.objects.get(user_id = self.request.user.pk) # 
        # context["posts_count"] = Post.objects.filter(author_id = profile) # 
        # context["my_friends"] = Friendship.objects.filter(profile2 = profile, accepted = True) #
        # context["all_requests"] = Friendship.objects.filter(profile2 = profile) #
        # context["all_users"] = Profile.objects.all() #
        # context["users"] = User.objects.all() 
        # author_avatars = {} #
        # for author in Profile.objects.filter(id__in=Post.objects.values_list('author_id', flat=True)): #
        #     avatar = Avatar.objects.filter(profile=author, shown=True, active=True).first() #
        #     author_avatars[author.id] = avatar #
        # for group in ChatGroup.objects.all(): #
        #     for member in group.members.all(): #
        #         if member.id not in author_avatars: #
        #             avatar = Avatar.objects.filter(profile=member, shown=True, active=True).first() #
        #             author_avatars[member.id] = avatar #
        # for friend_ship in Friendship.objects.all(): #
        #     if friend_ship.profile1 == Profile.objects.get(user_id = self.request.user.pk): #
        #         if friend_ship.profile2.id not in author_avatars: #
        #             avatar = Avatar.objects.filter(profile=friend_ship.profile2, shown=True, active=True).first()#
        #             author_avatars[friend_ship.profile2.id] = avatar #
        #     if friend_ship.profile2 == Profile.objects.get(user_id = self.request.user.pk): #
        #         if friend_ship.profile1.id not in author_avatars: #
        #             avatar = Avatar.objects.filter(profile=friend_ship.profile1, shown=True, active=True).first() #
        #             author_avatars[friend_ship.profile1.id] = avatar #


        # context['author_avatars'] = author_avatars #
        # context["my_avatars"] = Avatar.objects.filter(profile_id = profile.id) #
        # context['all_groups'] = ChatGroup.objects.all() #
        # context["current_user"] = profile #
        # context['all_views'] = Post.objects.none() #
        # for post in Post.objects.filter(author = profile): #  
        #     context['all_views'] = context['all_views'] | post.views.all() #
        return context #
 #   
class MyDeleteView(DeleteView):
    template_name = "delete_post/index.html" #
    model = Post #
    success_url = reverse_lazy("main") #
#
class EditView(UpdateView):
    model = Post # 
    form_class = PostFormEdit #
    template_name = 'edit/edit_form.html' #
    success_url = '/'#
    #
    def form_valid(self, form):
        form.instance.user = self.request.user  #
        return super().form_valid(form) #
#
class MyLogoutView(LogoutView):
    next_page = reverse_lazy('authorithation') #
 #
class PostDataView(View):
    #
    def post(self, request, post_pk):
        user_post = [Post.objects.get(pk = post_pk)] #
        return JsonResponse(serializers.serialize("json", user_post), safe=False) #

#
class UserUpdateView( UpdateView):
    model = User # 
    form_class = UserUpdateForm #
    template_name = 'main/index.html' #
    success_url = reverse_lazy("main") #
#
    def get_object(self):
        return self.request.user #
#
    def form_valid(self, form):
        response = super().form_valid(form) #
        return response #
#
def get_likes(request,  post_pk):
    post = Post.objects.get(id = post_pk) #
    profile = Profile.objects.get(user_id = request.user.id)  #
    post.likes.add(profile) #
    post.save() #
    return redirect("/") #

def get_all_info(request):
    profile_id = request.user.profile.id
    all_posts = Post.objects.filter(author_id = profile_id)
    all_posts_count = len(all_posts)
    all_views = []
    for post in all_posts:
        if post.views:
            for view in post.views.all():
                all_views.append(view.id)
    my_friends_1 = Friendship.objects.filter(profile1_id = profile_id, accepted = True)
    my_friends_2 = Friendship.objects.filter(profile2_id = profile_id, accepted = True)
    all_my_friends = my_friends_1.union(my_friends_2)
    all_requests = Friendship.objects.filter(profile2_id = profile_id, accepted = False)
    requests_data = serializers.serialize('json', all_requests)
    return JsonResponse({
                        "all_posts_count": all_posts_count,
                        "all_views": len(all_views),
                        "my_friends": len(all_my_friends),
                        "all_requests": requests_data
                         })