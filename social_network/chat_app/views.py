from django.views.generic import TemplateView, FormView, UpdateView
from user_app.models import Friendship, Avatar
from .forms import MessageForm
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from .models import ChatGroup, ChatMessage
import json
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from user_app.models import Profile


# Create your views here.
class ChatsView(TemplateView):
    template_name = "all_chats/all_chats.html"

    def dispatch(self, request, *args, **kwargs):
        if not Profile.objects.filter(user_id=request.user.id).exists():
            return redirect("registration")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем профиль текущего пользователя
        my_profile = Profile.objects.select_related('user').get(user_id=self.request.user.id)
        context["current_user"] = my_profile

        # Предзагружаем все нужные аватары
        all_avatars = Avatar.objects.filter(shown=True, active=True).select_related('profile')

        # Собираем друзей (можно дооптимизировать, если Friendship связан с Profile через foreign key)
        context["friends"] = Friendship.objects.filter(accepted=True)

        # Оптимизированная выборка групп чатов
        context["all_groups"] = ChatGroup.objects.select_related("admin").prefetch_related("members")

        # Заполнение словаря автор-аватар
        author_avatars = {
            avatar.profile_id: avatar for avatar in all_avatars
        }
        context["author_avatars"] = author_avatars

        # Участники группы по кукам
        ids_str = self.request.COOKIES.get('group_members')
        if ids_str:
            member_ids = ids_str.strip().split()
            context["members_group"] = Profile.objects.filter(id__in=member_ids)
        else:
            context["members_group"] = Profile.objects.none()

        return context

    def post(self, request, *args, **kwargs):
        selected_ids = request.POST.getlist('friends')
        if selected_ids:
            ids_str = " ".join(selected_ids)
            response = redirect('all_chats')
            response.set_cookie('group_members', ids_str)
            return response

        # Создание группы
        group_name = request.POST.get("group_name")
        group_avatar = request.FILES.get("add-image-avatar")
        ids_str = request.COOKIES.get("group_members", "")
        member_ids = ids_str.strip().split()

        # Получаем всех нужных участников одним запросом
        members = Profile.objects.filter(id__in=member_ids)

        # Получаем админа (текущего пользователя)
        admin = Profile.objects.get(user_id=self.request.user.id)

        # Создаём группу
        group = ChatGroup.objects.create(
            name=group_name,
            avatar=group_avatar,
            admin=admin
        )

        # Добавляем участников и текущего пользователя
        group.members.set(members)
        group.members.add(admin)

        response = redirect('all_chats')
        response.delete_cookie('group_members')
        return response

class ChatView(FormView):
    template_name = "chat/chat.html"
    form_class = MessageForm

    def dispatch(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user_id=request.user.pk)
            chat = ChatGroup.objects.prefetch_related('members').get(pk=self.kwargs["chat_pk"])
        except (Profile.DoesNotExist, ChatGroup.DoesNotExist):
            return redirect("all_chats")

        if profile not in chat.members.all():
            return redirect("all_chats")

        if not Profile.objects.filter(user_id=request.user.id).exists():
            return redirect("registration")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat_pk = self.kwargs["chat_pk"]

        group = ChatGroup.objects.select_related('admin').prefetch_related('members').get(pk=chat_pk)

        messages = ChatMessage.objects.filter(chat_group=group).select_related('author')

        my_profile = Profile.objects.select_related('user').get(user_id=self.request.user.id)
        friends = Friendship.objects.filter(accepted=True)
        all_groups = ChatGroup.objects.prefetch_related('members')

        # Предзагружаем только нужные профили для аватаров
        members_profiles = list(group.members.all())
        author_ids = [p.id for p in members_profiles]
        avatars = Avatar.objects.filter(profile_id__in=author_ids, shown=True, active=True)
        author_avatars = {avatar.profile_id: avatar for avatar in avatars}

        context.update({
            "chat_group": group,
            "messages": messages,
            "current_user": my_profile,
            "friends": friends,
            "all_groups": all_groups,
            "members_group": members_profiles,
            "author_avatars": author_avatars
        })

        return context

    def post(self, request, *args, **kwargs):
        # Добавление участников в куки (из all_chats)
        if request.POST.getlist('friends'):
            selected_ids = request.POST.getlist('friends')
            response = redirect('all_chats')
            response.set_cookie('group_members', " ".join(selected_ids))
            return response

        # Создание группы
        elif request.POST.get("group_name"):
            group_name = request.POST.get("group_name")
            group_avatar = request.FILES.get("add-image-avatar")

            member_ids = request.COOKIES.get("group_members", "").strip().split()
            members = Profile.objects.filter(id__in=member_ids)

            admin_profile = Profile.objects.get(user_id=request.user.id)
            group = ChatGroup.objects.create(
                name=group_name,
                avatar=group_avatar,
                admin=admin_profile
            )
            group.members.set(members)
            group.members.add(admin_profile)

            response = redirect('all_chats')
            response.delete_cookie('group_members')
            return response

        # Редактирование группы (название/аватар)
        elif not request.POST.getlist('edit_friends') and not request.POST.get("chat_hidden_input"):
            group = ChatGroup.objects.get(pk=self.kwargs['chat_pk'])
            new_name = request.POST.get("edit_group_name")
            new_avatar = request.FILES.get("edit-image-avatar")

            if new_name:
                group.name = new_name
            if new_avatar:
                group.avatar = new_avatar
            group.save()

            response = redirect('chat', self.kwargs['chat_pk'])
            response.delete_cookie("get_friends")
            return response

        # Обновление списка участников
        else:
            members_id = request.POST.getlist('edit_friends')
            group = ChatGroup.objects.get(pk=self.kwargs['chat_pk'])
            my_profile = Profile.objects.get(user_id=request.user.id)

            group.members.set(members_id)
            group.members.add(my_profile)

            response = redirect('chat', self.kwargs['chat_pk'])
            response.set_cookie("get_friends", "1234")
            return response

    def get_success_url(self):
        return reverse("chat", kwargs={"chat_pk": self.kwargs["chat_pk"]})


    
def create_chat(request, user_pk):
    connected_user = Profile.objects.get(pk = user_pk)
    current_user = Profile.objects.get(user_id = request.user.pk)
    user_group_with_us = ChatGroup.objects.filter(members = connected_user, is_personal_chat = True).filter(members =  current_user).first()

    if not user_group_with_us:
        personal_chat = ChatGroup.objects.create(
            name = f"Чат {connected_user} з {current_user}",
            is_personal_chat = True,
            admin_id = current_user.pk
        )
        personal_chat.members.set([current_user, connected_user])
        personal_chat.save()
    else:
        personal_chat = user_group_with_us
    return redirect("chat", personal_chat.pk)

def delete_user_from_cookies(request, user_pk):
    response = JsonResponse({})
    ids_str = request.COOKIES.get('group_members')
    if ids_str:
        member_ids = ids_str.strip().split()
        member_ids.remove(str(user_pk))  
        ids_str = " ".join(member_ids)
    response.set_cookie('group_members', ids_str)
    return response

def delete_chat(request, chat_pk):
    chat = ChatGroup.objects.get(pk = chat_pk)
    chat.delete()
    return redirect("all_chats")

def exit_group(request, chat_pk):
    profile = Profile.objects.get(user_id = request.user.id)
    chat = ChatGroup.objects.get(pk = chat_pk)
    if profile in chat.members.all():
        chat.members.remove(profile)
    return redirect("all_chats")

from django.shortcuts import render
# from user_app.models import Friendship, Avatar, Profile

@login_required
def ajax_chat_contacts(request):
    current_user = Profile.objects.get(user=request.user)
    friends = Friendship.objects.filter(
        accepted=True
    ).filter(
        profile1=current_user
    ) | Friendship.objects.filter(
        accepted=True,
        profile2=current_user
    )
    friends = friends.distinct()

    friend_profiles = []
    for f in friends:
        if f.profile1 == current_user:
            friend_profiles.append(f.profile2)
        else:
            friend_profiles.append(f.profile1)
    avatars = Avatar.objects.filter(profile__in=friend_profiles, shown=True, active=True)
    avatar_map = {a.profile_id: a for a in avatars}

    return render(request, "chat/ajax_contacts.html", {
        "friends": friend_profiles,
        "author_avatars": avatar_map,
    })
