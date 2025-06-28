from django.views.generic import TemplateView, FormView
from user_app.models import Profile, Friendship, Avatar
from .forms import MessageForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from .models import ChatGroup, ChatMessage
from django.http import JsonResponse
from django.db.models import Prefetch


class ChatsView(TemplateView):
    template_name = "all_chats/all_chats.html"

    def dispatch(self, request, *args, **kwargs):
        if not Profile.objects.filter(user_id=request.user.id).exists():
            return redirect("registration")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST.getlist('friends'):
            ids_str = " ".join(request.POST.getlist('friends'))
            response = redirect('all_chats')
            response.set_cookie('group_members', ids_str)
            return response

        group_name = request.POST.get("group_name")
        group_avatar = request.FILES.get("add-image-avatar")
        member_ids = request.COOKIES.get("group_members", "").strip().split()
        members = Profile.objects.filter(id__in=member_ids)

        admin = Profile.objects.select_related('user').get(user_id=request.user.id)
        group = ChatGroup.objects.create(name=group_name, avatar=group_avatar, admin=admin)
        group.members.set(members)
        group.members.add(admin)

        response = redirect('all_chats')
        response.delete_cookie('group_members')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_profile = Profile.objects.select_related('user').get(user_id=self.request.user.id)
        all_profiles = Profile.objects.all().prefetch_related(
            Prefetch('avatar_set', queryset=Avatar.objects.filter(shown=True, active=True), to_attr='active_avatars')
        )

        author_avatars = {p.id: (p.active_avatars[0] if p.active_avatars else None) for p in all_profiles}
        member_ids = self.request.COOKIES.get('group_members', "").strip().split()

        context.update({
            "all_avatars": Avatar.objects.all(),
            "current_user": my_profile,
            "friends": Friendship.objects.filter(accepted=True),
            "all_groups": ChatGroup.objects.prefetch_related('members'),
            "members_group": Profile.objects.filter(id__in=member_ids) if member_ids else Profile.objects.none(),
            "author_avatars": author_avatars
        })
        return context


class ChatView(FormView):
    template_name = "chat/chat.html"
    form_class = MessageForm

    def dispatch(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user_id=request.user.pk)
            chat = ChatGroup.objects.prefetch_related('members').get(id=self.kwargs["chat_pk"])
        except (Profile.DoesNotExist, ChatGroup.DoesNotExist):
            return redirect("all_chats")

        if profile not in chat.members.all():
            return redirect("all_chats")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat_pk = self.kwargs["chat_pk"]
        group = ChatGroup.objects.prefetch_related('members').get(id=chat_pk)
        current_user = Profile.objects.select_related('user').get(user_id=self.request.user.id)

        all_profiles = Profile.objects.all().prefetch_related(
            Prefetch('avatar_set', queryset=Avatar.objects.filter(shown=True, active=True), to_attr='active_avatars')
        )
        author_avatars = {p.id: (p.active_avatars[0] if p.active_avatars else None) for p in all_profiles}

        context.update({
            "chat_group": group,
            "all_avatars": Avatar.objects.all(),
            "current_user": current_user,
            "friends": Friendship.objects.filter(accepted=True),
            "all_groups": ChatGroup.objects.prefetch_related('members'),
            "messages": ChatMessage.objects.filter(chat_group=group).select_related('author'),
            "members_group": group.members.all(),
            "author_avatars": author_avatars
        })
        return context

    def post(self, request, *args, **kwargs):
        # Creating new group
        if request.POST.getlist('friends'):
            ids_str = " ".join(request.POST.getlist('friends'))
            response = redirect('all_chats')
            response.set_cookie('group_members', ids_str)
            return response

        if request.POST.get("group_name"):
            group_name = request.POST.get("group_name")
            group_avatar = request.FILES.get("add-image-avatar")
            member_ids = request.COOKIES.get("group_members", "").strip().split()
            members = Profile.objects.filter(id__in=member_ids)
            admin = Profile.objects.get(user_id=request.user.id)

            group = ChatGroup.objects.create(name=group_name, avatar=group_avatar, admin=admin)
            group.members.set(members)
            group.members.add(admin)

            response = redirect('all_chats')
            response.delete_cookie('group_members')
            return response

        # Editing existing group
        group = ChatGroup.objects.get(id=self.kwargs["chat_pk"])

        if request.POST.get("edit_group_name"):
            group.name = request.POST.get("edit_group_name")
            new_avatar = request.FILES.get("edit-image-avatar")
            if new_avatar:
                group.avatar = new_avatar
            group.save()
            response = redirect('chat', self.kwargs['chat_pk'])
            response.delete_cookie("get_friends")
            return response

        if request.POST.getlist('edit_friends'):
            members_id = request.POST.getlist('edit_friends')
            current_user = Profile.objects.get(user_id=request.user.id)
            group.members.set(members_id)
            group.members.add(current_user)
            response = redirect('chat', self.kwargs['chat_pk'])
            response.set_cookie("get_friends", "1234")
            return response

        return redirect('chat', self.kwargs['chat_pk'])

    def get_success_url(self):
        return reverse("chat", kwargs={"chat_pk": self.kwargs["chat_pk"]})


def create_chat(request, user_pk):
    connected_user = Profile.objects.get(pk=user_pk)
    current_user = Profile.objects.get(user_id=request.user.pk)

    existing_chat = ChatGroup.objects.filter(
        is_personal_chat=True,
        members=connected_user
    ).filter(members=current_user).first()

    if not existing_chat:
        chat = ChatGroup.objects.create(
            name=f"Чат {connected_user} з {current_user}",
            is_personal_chat=True,
            admin=current_user
        )
        chat.members.set([connected_user, current_user])
    else:
        chat = existing_chat

    return redirect("chat", chat.pk)


def delete_user_from_cookies(request, user_pk):
    ids_str = request.COOKIES.get('group_members', "")
    member_ids = ids_str.strip().split()
    member_ids = [id for id in member_ids if id != str(user_pk)]
    response = JsonResponse({})
    response.set_cookie('group_members', " ".join(member_ids))
    return response


def delete_chat(request, chat_pk):
    ChatGroup.objects.filter(pk=chat_pk).delete()
    return redirect("all_chats")


def exit_group(request, chat_pk):
    profile = Profile.objects.get(user_id=request.user.id)
    chat = ChatGroup.objects.prefetch_related('members').get(pk=chat_pk)
    chat.members.remove(profile)
    return redirect("all_chats")
