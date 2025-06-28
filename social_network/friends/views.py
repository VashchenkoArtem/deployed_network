from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from user_app.models import Friendship, Avatar, Profile
from post_app.models import Album, Post
from django.contrib.auth.models import User
from django.urls import reverse_lazy

# 🔹 Оптимизация общего запроса аватаров по списку профилей
def get_author_avatars(profiles):
    avatars = Avatar.objects.filter(profile__in=profiles, shown=True, active=True).only("profile_id", "image")
    avatar_map = {a.profile_id: a for a in avatars}
    return {p.id: avatar_map.get(p.id) for p in profiles}

# 🔹 FriendsView
class FriendsView(TemplateView):
    template_name = "friends/friends.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        profile = Profile.objects.select_related("user").get(user=current_user)
        all_profiles = Profile.objects.exclude(user=current_user)[:6]

        context.update({
            "all_recommended": all_profiles,
            "all_friends": Friendship.objects.filter(accepted=True).only("profile1_id", "profile2_id")[:6],
            "all_requests": Friendship.objects.filter(profile2=profile, accepted=False)[:6],
            "all_avatars": Avatar.objects.only("profile_id", "image"),
            "current_user": profile,
            "author_avatars": get_author_avatars(all_profiles),
        })
        return context

    def dispatch(self, request, *args, **kwargs):
        if not Profile.objects.filter(user=request.user).exists():
            return redirect("registration")
        return super().dispatch(request, *args, **kwargs)

# 🔹 AllFriendsView
class AllFriendsView(TemplateView):
    template_name = "all_friends/all_friends.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = Profile.objects.get(user=self.request.user)
        all_profiles = Profile.objects.all()
        context.update({
            "all_friends": Friendship.objects.filter(accepted=True).only("profile1_id", "profile2_id"),
            "all_avatars": Avatar.objects.only("profile_id", "image"),
            "current_user": current_user,
            "author_avatars": get_author_avatars(all_profiles),
        })
        return context

    def dispatch(self, request, *args, **kwargs):
        if not Profile.objects.filter(user=request.user).exists():
            return redirect("registration")
        return super().dispatch(request, *args, **kwargs)

# 🔹 RequestView
class RequestView(TemplateView):
    template_name = "all_requests/requests.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        all_profiles = Profile.objects.all()
        context.update({
            "all_requests": Friendship.objects.filter(profile2=profile, accepted=False).only("profile1_id", "profile2_id"),
            "all_avatars": Avatar.objects.only("profile_id", "image"),
            "author_avatars": get_author_avatars(all_profiles),
        })
        return context

    def dispatch(self, request, *args, **kwargs):
        if not Profile.objects.filter(user=request.user).exists():
            return redirect("registration")
        return super().dispatch(request, *args, **kwargs)

# 🔹 RecommendedView
class RecommendedView(TemplateView):
    template_name = "recommended/recommended.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_profiles = Profile.objects.exclude(user=self.request.user)
        context.update({
            "all_recommended": all_profiles,
            "all_avatars": Avatar.objects.only("profile_id", "image"),
            "author_avatars": get_author_avatars(all_profiles),
        })
        return context

    def dispatch(self, request, *args, **kwargs):
        if not Profile.objects.filter(user=request.user).exists():
            return redirect("registration")
        return super().dispatch(request, *args, **kwargs)

# 🔹 FriendProfileView
class FriendProfileView(TemplateView):
    template_name = 'friend_profile/friend_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        friend_pk = self.kwargs['friend_pk']
        friend_profile = Profile.objects.select_related('user').get(user_id=friend_pk)
        current_profile = Profile.objects.get(user=self.request.user)

        # Посты и просмотры
        posts = Post.objects.filter(author=friend_profile).prefetch_related("views")
        views = sum((list(post.views.all()) for post in posts), [])

        # Аватар
        avatar = Avatar.objects.filter(profile=friend_profile, shown=True, active=True).first()

        # Запрос дружбы
        current_request = Friendship.objects.filter(
            profile1=friend_profile, profile2=current_profile
        ).union(
            Friendship.objects.filter(profile2=friend_profile, profile1=current_profile)
        ).first()

        context.update({
            'friend': friend_profile,
            'avatar': avatar,
            'all_avatars': Avatar.objects.only("profile_id", "image"),
            'all_posts': posts.order_by('-id'),
            'posts_count': posts.count(),
            'current_request': current_request,
            'all_views': views,
            'all_albums': Album.objects.filter(author=friend_profile),
            'my_friends': Friendship.objects.filter(profile2=friend_profile, accepted=True).union(
                Friendship.objects.filter(profile1=friend_profile, accepted=True)
            ),
        })
        return context

    def dispatch(self, request, *args, **kwargs):
        if not Profile.objects.filter(user=request.user).exists():
            return redirect("registration")
        return super().dispatch(request, *args, **kwargs)

# 🔹 Удаление запроса
def delete_request(request, pk):
    current_user = Profile.objects.get(user=request.user)
    friend_user = Profile.objects.get(user_id=pk)

    Friendship.objects.filter(profile1=current_user, profile2=friend_user).delete()
    Friendship.objects.filter(profile2=current_user, profile1=friend_user).delete()

    return redirect("main_friends")

# 🔹 Удаление рекомендации (можно кастомизировать под метку "скрыть")
def delete_recommended(request, pk):
    # Допиши здесь сохранение "отказа" в рекомендациях, если нужно
    return redirect("main_friends")

# 🔹 Удаление друга
def delete_friend(request, pk):
    current_user = Profile.objects.get(user=request.user)
    friend_user = Profile.objects.get(user_id=pk)

    Friendship.objects.filter(profile1=current_user, profile2=friend_user).delete()
    Friendship.objects.filter(profile2=current_user, profile1=friend_user).delete()

    return redirect("main_friends")

# 🔹 Подтверждение заявки в друзья
def confirm_friend(request, pk):
    current_profile = Profile.objects.get(user=request.user)
    friend_profile = Profile.objects.get(user_id=pk)

    request_obj = Friendship.objects.get(profile1=friend_profile, profile2=current_profile)
    request_obj.accepted = True
    request_obj.save()

    return redirect("main_friends")

# 🔹 Отправка заявки
def request_to_user(request, pk):
    current_user = Profile.objects.get(user=request.user)
    request_user = Profile.objects.get(user_id=pk)

    if not Friendship.objects.filter(profile1=current_user, profile2=request_user).exists() and \
       not Friendship.objects.filter(profile1=request_user, profile2=current_user).exists():
        Friendship.objects.create(profile1=current_user, profile2=request_user, accepted=False)

    return redirect("main_friends")
