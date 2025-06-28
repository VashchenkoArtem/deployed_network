from django.views.generic import TemplateView, FormView, UpdateView
from user_app.models import Friendship, Avatar
from .forms import MessageForm
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from .models import ChatGroup, ChatMessage
import json
from django.urls import reverse
from django.http import JsonResponse
from user_app.models import Profile


# Create your views here.
class ChatsView(TemplateView):
    template_name = "all_chats/all_chats.html"
    def dispatch(self, request, *args, **kwargs):
        if not Profile.objects.filter(user_id = request.user.id).exists():
            return redirect("registration")
        else:   
            return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        if request.POST.getlist('friends'):  
            selected_ids = request.POST.getlist('friends')
            ids_str = " ".join(selected_ids)
            response = redirect('all_chats') 
            response.set_cookie('group_members', ids_str)
            return response

        else:
            group_name = request.POST.get("group_name")
            group_avatar = request.FILES.get("add-image-avatar")

            ids_str = request.COOKIES.get("group_members", "")
            member_ids = ids_str.strip().split()
            members = Profile.objects.filter(id__in=member_ids)
            admin = Profile.objects.get(user_id = self.request.user.id)
            group = ChatGroup.objects.create(
                name=group_name,
                avatar=group_avatar,
                admin = admin
            )

            my_profile = Profile.objects.get(user_id = self.request.user.pk)
            group.members.set(members)
            group.members.add(my_profile)
            

            response = redirect('all_chats')
            response.delete_cookie('group_members')
            return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_profiles = Profile.objects.all()
        my_profile = all_profiles.get(user_id=self.request.user.id)
        context["all_avatars"] = Avatar.objects.all()
        context["current_user"] = my_profile
        context["friends"] = Friendship.objects.filter(accepted=True)
        context["all_groups"] = ChatGroup.objects.all()
        context["members_group"] = all_profiles.none()
        author_avatars = {}
        for author in all_profiles:
            avatar = Avatar.objects.filter(profile=author, shown=True, active=True).first()
            author_avatars[author.id] = avatar
        context["author_avatars"] = author_avatars
        ids_str = self.request.COOKIES.get('group_members')
        if ids_str:
            member_ids = ids_str.strip().split()
            context["members_group"] = all_profiles.filter(id__in=member_ids)
        return context

class ChatView(FormView):
    template_name = "chat/chat.html"
    form_class = MessageForm
    def dispatch(self, request, *args, **kwargs):
        profile = Profile.objects.get(user_id = request.user.pk)
        chat_pk = self.kwargs["chat_pk"]
        chat = ChatGroup.objects.get(id = chat_pk)
        if profile in chat.members.all():
            if not Profile.objects.filter(user_id = request.user.id).exists():
                return redirect("registration")
            else:   
                return super().dispatch(request, *args, **kwargs)
        elif profile not in chat.members.all():
            return redirect("all_chats")

    def get_context_data(self, **kwargs):
        context = super(ChatView, self).get_context_data(**kwargs)
        chat_pk = self.kwargs["chat_pk"]
        group = ChatGroup.objects.get(id = chat_pk)
        all_messages = ChatMessage.objects.filter(chat_group = group)
        
        context['chat_group'] = group
        context["all_avatars"] = Avatar.objects.all()
        context['current_user'] = Profile.objects.get(user_id = self.request.user.id)
        context["friends"] = Friendship.objects.filter(accepted = True)
        context['all_groups'] = ChatGroup.objects.all()
        context['messages'] = all_messages
        context["members_group"] = group.members.all()
        author_avatars = {}
        for author in Profile.objects.all():
            avatar = Avatar.objects.filter(profile=author, shown=True, active=True).first()
            author_avatars[author.id] = avatar
        context["author_avatars"] = author_avatars
        return context
    def post(self, request, *args, **kwargs):
        # ChatsView

        if request.POST.getlist('friends'):  
            selected_ids = request.POST.getlist('friends')
            ids_str = " ".join(selected_ids)
            response = redirect('all_chats') 
            response.set_cookie('group_members', ids_str)
            return response
        elif request.POST.getlist("group_name"):
            group_name = request.POST.get("group_name")
            group_avatar = request.FILES.get("add-image-avatar")

            ids_str = request.COOKIES.get("group_members", "")
            member_ids = ids_str.strip().split()
            members = Profile.objects.filter(id__in=member_ids)

            group = ChatGroup.objects.create(
                name=group_name,
                avatar=group_avatar,
                admin_id=self.request.user.id
            )

            my_profile = Profile.objects.get(user_id = self.request.user.pk)
            group.members.set(members)
            group.members.add(my_profile)
        
            response = redirect('all_chats')
            response.delete_cookie('group_members')
        # ChatView

        elif not request.POST.getlist('edit_friends') and not request.POST.get("chat_hidden_input"):
            response = redirect('chat', self.kwargs['chat_pk'])
            try:
                new_group_name = request.POST.get("edit_group_name")
                new_group_avatar = request.FILES.get("edit-image-avatar")
                group = ChatGroup.objects.get(id = self.kwargs['chat_pk'])
                group.name = new_group_name
                if new_group_avatar:
                    group.avatar = new_group_avatar
                    group.save()
                if new_group_name:
                    group.name = new_group_name
                    group.save()
                
                response.delete_cookie("get_friends")
                return response
            except:
                return response
        else:
            members_id = request.POST.getlist('edit_friends')
            response = redirect('chat', self.kwargs['chat_pk'])
            chat_pk = self.kwargs["chat_pk"]
            my_profile = Profile.objects.get(user_id = self.request.user.id)
            group = ChatGroup.objects.get(id = chat_pk)
            group.members.set(members_id)
            group.members.add(my_profile)
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