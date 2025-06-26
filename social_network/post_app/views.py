from django.views.generic.edit import CreateView
from main.forms import PostForm
from .models import Post, Tag
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.core import serializers
from django.views.generic import TemplateView
from user_app.models import Friendship, Avatar, Profile
from post_app.models import Post,Image, Tag, Link
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseNotAllowed


class MyPublicationsView(CreateView):
    template_name = "my_publications/index.html"
    form_class = PostForm
    success_url = reverse_lazy("my_pubs")
    def form_valid(self, form):
        profile = Profile.objects.get(user_id=self.request.user.pk)
        form.instance.author = profile
        response = super().form_valid(form)
        urls = self.request.POST.getlist('url')   
        for url in urls:
            url = Link.objects.create(post = self.object, url = url) 
        
        files = self.request.FILES.getlist('images')
        for file in files:
            image = Image.objects.create(filename = f"photo-{self.object}", file=file)
            self.object.images.add(image)
        return response
    def dispatch(self, request, *args, **kwargs):
        if not Profile.objects.filter(user_id = request.user.id).exists():
            return redirect("registration")
        current_user = Profile.objects.get(user_id = self.request.user.pk)
        user_posts = Post.objects.all()
        if len(user_posts) > 0:
            for post_view in user_posts:
                post_view.views.add(current_user)
                post_view.save()
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(MyPublicationsView, self).get_context_data(**kwargs)
        profile = Profile.objects.get(user_id = self.request.user.pk)
        context["posts"] = Post.objects.filter(author_id = profile.id).order_by('-id')
        context["tags"] = Tag.objects.all()
        context['people'] = Profile.objects.get(user_id = self.request.user.pk)
        context["all_urls"] = Link.objects.all()
        context['all_peoples'] = Profile.objects.all()
        context["posts_count"] = Post.objects.filter(author_id = profile)
        context["my_friends"] = Friendship.objects.filter(profile2 = profile, accepted = True)
        context["all_requests"] = Friendship.objects.filter(profile2 = profile)
        context["all_users"] = Profile.objects.all()
        avatars = {}
        author_ids = Post.objects.values_list('author_id', flat=True).distinct()
        for author_id in author_ids:
            avatar = Avatar.objects.filter(profile_id=author_id, shown=True, active=True).first()
            avatars[author_id] = avatar
        context["my_avatars"] = Avatar.objects.filter(profile_id = profile.id)
        context['all_views'] = Post.objects.none()
        for post in Post.objects.filter(author = profile):    
            context['all_views'] = context['all_views'] | post.views.all()
        return context 



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