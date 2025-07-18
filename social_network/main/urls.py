from django.urls import path
from social_network.settings import DEBUG, MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static
from .views import (
    MyDeleteView, EditView, MyLogoutView, PostDataView, UserUpdateView,
    get_likes, get_all_info, get_all_tags, load_posts
)



urlpatterns = [
    path('delete/<int:pk>', MyDeleteView.as_view(), name = "delete"),
    path('edit/<int:pk>', EditView.as_view(), name='edit'),
    path('logout/', MyLogoutView.as_view(), name = "logout"),
    path('check_info/<int:post_pk>', PostDataView.as_view(), name = "check_info"),
    path('update/', UserUpdateView.as_view(), name='update_user'),
    path("add_like/<int:post_pk>", get_likes, name  = "get_likes"),
    path("get_info/", get_all_info, name = "get_all_info"),
    path("get_all_tags/", get_all_tags, name = "get_all_tags"),


]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)