from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import View
from .forms import PostForm, PostFormEdit, UserUpdateForm
from post_app.models import Post, Image, Tag, Link
from user_app.models import Friendship, Avatar, Profile
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.models import User
from chat_app.models import ChatGroup
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET
from django.utils.decorators import method_decorator
from django.views import View


class MainView(CreateView):
    template_name = "main/index.html"
    form_class = PostForm
    success_url = "/"

    def form_valid(self, form):
        profile = Profile.objects.get(user_id=self.request.user.pk)
        form.instance.author = profile
        response = super().form_valid(form)
        urls = self.request.POST.getlist('url')
        for url in urls:
            Link.objects.create(post=self.object, url=url)
        files = self.request.FILES.getlist('images')
        for file in files:
            image = Image.objects.create(filename=f"photo-{self.object}", file=file)
            self.object.images.add(image)
        return response

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if not Profile.objects.filter(user_id=request.user.id).exists():
            return redirect("registration")
        current_user = Profile.objects.get(user_id=request.user.pk)
        user_posts = Post.objects.order_by("-id")[:3]
        for post_view in user_posts:
            post_view.views.add(current_user)
        response.set_cookie("user_id", request.user.id)
        return response

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context["posts"] = Post.objects.order_by('-id')[:3]
            context["tags"] = Tag.objects.all()
            profile_id = self.request.user.profile.id
            context["profile_id"] = profile_id
            context['author_avatars'] = {}
            context["my_avatar"] = Avatar.objects.filter(profile_id = profile_id).first()
            context['all_groups'] = ChatGroup.objects.none()
            context["all_requests"] = Friendship.objects.filter(profile2_id=profile_id)
            return context
        except:
            return redirect("registration")

class MyDeleteView(DeleteView):
    template_name = "delete_post/index.html"
    model = Post
    success_url = reverse_lazy("main")

class EditView(UpdateView):
    model = Post
    form_class = PostFormEdit
    template_name = 'edit/edit_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class MyLogoutView(LogoutView):
    next_page = reverse_lazy('authorithation')

class PostDataView(View):
    def post(self, request, post_pk):
        user_post = [Post.objects.get(pk=post_pk)]
        return JsonResponse(serializers.serialize("json", user_post), safe=False)

class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'main/index.html'
    success_url = reverse_lazy("main")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        return super().form_valid(form)

def get_likes(request, post_pk):
    post = Post.objects.get(id=post_pk)
    profile = Profile.objects.get(user_id=request.user.id)
    post.likes.add(profile)
    post.save()
    return redirect("/")

def get_all_info(request):
    profile_id = request.user.profile.id
    all_posts = Post.objects.filter(author_id=profile_id)
    all_views = [view.id for post in all_posts for view in post.views.all()]
    my_friends_1 = Friendship.objects.filter(profile1_id=profile_id, accepted=True)
    my_friends_2 = Friendship.objects.filter(profile2_id=profile_id, accepted=True)
    all_my_friends = my_friends_1.union(my_friends_2)
    all_requests = Friendship.objects.filter(profile2_id=profile_id)
    request_data = serializers.serialize('json', all_requests)
    return JsonResponse({
        "all_posts_count": all_posts.count(),
        "all_views": len(all_views),
        "my_friends": all_my_friends.count(),
        "all_requests": request_data,
        "profile_id": profile_id
    })

def get_all_tags(request):
    tags = Tag.objects.all()
    tags_data = serializers.serialize('json', tags)
    return JsonResponse({"tags": tags_data})


def load_posts(request):
    page = int(request.GET.get("page", 1))
    posts = Post.objects.order_by("-id")
    paginator = Paginator(posts, 3)
    page_obj = paginator.get_page(page)

    # Получаем список author_id из объектов текущей страницы (в памяти)
    author_ids = list(set(post.author_id for post in page_obj.object_list))

    authors = Profile.objects.filter(id__in=author_ids)

    author_avatars = {}
    for author in authors:
        avatar = Avatar.objects.filter(profile=author, shown=True, active=True).first()
        author_avatars[author.id] = avatar

    html = render_to_string(
        "partials/post_block.html",
        {
            "posts": page_obj,
            "author_avatars": author_avatars,
        }
    )
    return JsonResponse(html, safe=False)
