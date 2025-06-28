from django.views.generic.edit import CreateView, DeleteView, UpdateView
from main.forms import PostForm, PostFormEdit, UserUpdateForm 
from .models import Post, Tag
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.core import serializers
from django.views.generic import TemplateView
from user_app.models import Friendship, Avatar, Profile
from post_app.models import Post,Image, Tag, Link
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.generic import View
from django.contrib.auth.views import LogoutView
from django.contrib.auth.models import User
from chat_app.models import ChatGroup



# Створюємо класс відображення моїх відображень
class MyPublicationsView(CreateView):
    template_name = "my_publications/index.html" # Шаблон моїх публікацій 
    form_class = PostForm # Створюємо PostForm 
    success_url = reverse_lazy("my_pubs") # Створюємо успішний юрл сторінки мої публікації
    # Створюємо функцію валідації форми 
    # def form_valid(self, form):
    #     profile = Profile.objects.get(user_id=self.request.user.pk) # Створюємо функцію яка отримує обьекти юзер айди
    #     form.instance.author = profile # Створюємо функцію образця форми 
    #     response = super().form_valid(form) # Функція яка переверяє валідність відповіді
    #     urls = self.request.POST.getlist('url')#зберігаємо Post і отримуємо список
    #     for url in urls:#створємо цикл для url в  urls 
    #         url = Link.objects.create(post = self.object, url = url)#функція яка  створює шлях до обьектів
        
    #     files = self.request.FILES.getlist('images')#зберігаємо файли по списку"images"
    #     for file in files:#створюємо цикл  file в files
    #         image = Image.objects.create(filename = f"photo-{self.object}", file=file)#створюємо обьект створення зображень
    #         self.object.images.add(image)#функція збереження обьекті
    #     return response
    
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
    
    # def dispatch(self, request, *args, **kwargs):
    #     if not Profile.objects.filter(user_id = request.user.id).exists():
    #         return redirect("registration")
    #     current_user = Profile.objects.get(user_id = self.request.user.pk)
    #     user_posts = Post.objects.all()
    #     if len(user_posts) > 0:
    #         for post_view in user_posts:
    #             post_view.views.add(current_user)
    #             post_view.save()
    #     return super().dispatch(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if not Profile.objects.filter(user_id = request.user.id).exists(): # 
            return redirect("registration") #
        current_user = Profile.objects.get(user_id = self.request.user.pk) #
        user_posts = Post.objects.all()[:3] #
        if len(user_posts) > 0: #
            for post_view in user_posts: #
                post_view.views.add(current_user) #
                post_view.save() #
        response.set_cookie("user_id", request.user.id)
        return response #
    
    
    def get_context_data(self, **kwargs):
        context = super(MyPublicationsView, self).get_context_data(**kwargs) 
        my_posts = Post.objects.filter(author_id = self.request.user.profile.id).order_by('-id')[:3] #
        context["posts"] = my_posts # 
        context["tags"] = Tag.objects.all() # 
        author_avatars = {} #
        context['author_avatars'] = author_avatars 
        context['all_groups'] = ChatGroup.objects.none() #
        profile_id = self.request.user.profile.id

        context["all_requests"] = Friendship.objects.filter(profile2_id = profile_id) #
        return context #



# def redact_data(request, post_pk):
#     if request.method == 'POST':
#         post = Post.objects.get(id=post_pk)
#         post_dict = {
#             'id': post.id,
#             'title': post.title,
#             'content': post.content,
#             'author': post.author.username,
#             # 'images': [img.file.url for img in post.images.all()],
#             # 'tags': [tag.name for tag in post.tags.all()],
#             'topic': post.topic, 
#         }

#         return JsonResponse(post_dict)
#     else:
#         return HttpResponseNotAllowed(['POST'])


def redact_data(request, post_pk):
    if request.method == "POST":
        try:
            post = Post.objects.get(pk=post_pk)
            link = Link.objects.filter(post=post).first() 
            return JsonResponse({
                "title": post.title,
                "topic": post.topic,
                "content": post.content,
                "link": link.url if link else "",
            })
        except Post.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)
    return JsonResponse({"error": "Invalid method"}, status=400)
def create_tag(request, tag_name):
    if not Tag.objects.filter(name = f"#{tag_name}").exists():
        Tag.objects.create(name = f"#{tag_name}")
    return redirect("my_pubs")


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
    all_requests = Friendship.objects.filter(profile2_id = profile_id)
    request_data = serializers.serialize('json', all_requests)
    return JsonResponse({
                        "all_posts_count": all_posts_count,
                        "all_views": len(all_views),
                        "my_friends": len(all_my_friends),
                        "all_requests": request_data,
                        "profile_id": profile_id
                        })
    
def get_all_tags(request):
    tags = Tag.objects.all()
    tags_data = serializers.serialize('json', tags)
    return JsonResponse({"tags": tags_data})



