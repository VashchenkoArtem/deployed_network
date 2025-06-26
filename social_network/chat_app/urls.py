from django.contrib import admin
from django.urls import path, include
from social_network.settings import DEBUG, MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path("all_chats/", ChatsView.as_view(), name = "all_chats"),
    path("all_chats/<int:chat_pk>", ChatView.as_view(), name = "chat"),
    path("all_chats/create_chat/<int:user_pk>", create_chat, name = "create_chat"),
    path("all_chats/delete_cookie_user/<int:user_pk>", delete_user_from_cookies, name = "delete_user_cookie"),
    # path("all_chats/edit_chat/<int:pk>", EditChat.as_view(), name = "edit_chat")
    path("all_chats/delete_chat/<int:chat_pk>", delete_chat, name = "delete_chat"),
    path("all_chats/exit_from_chat/<int:chat_pk>", exit_group, name = "exit_from_group")
]
if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)