"""
URL configuration for social_network project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from main.views import MainView
from .settings import DEBUG, MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static
from post_app.views import MyPublicationsView, redact_data, create_tag
from main.views import MainView, get_all_info, load_posts


urlpatterns = [
    path('admin/', admin.site.urls),
    path("user/", include("user_app.urls")),
    path("", MainView.as_view(), name = "main"),
    path("post/", include("main.urls")),
    path("my_publications/", MyPublicationsView.as_view(), name = "my_pubs"),
    path("check_info_post/<int:post_pk>", redact_data, name = "check_info_post"),
    path("settings/", include('settings_app.urls')),
    path("friends/", include('friends.urls')),
    path("chats/", include("chat_app.urls")),
    path("my_publications/create_tag/<str:tag_name>", create_tag, name = "create_tag"),
    path("get_info/", get_all_info, name = "get_all_info"),
    path('load_posts/', load_posts, name='load_posts'),
]
if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)