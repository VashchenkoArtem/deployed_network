from django.urls import path, include
from social_network.settings import DEBUG, MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path("main/", FriendsView.as_view(), name = "main_friends"),
    path("all_friends/", AllFriendsView.as_view(), name = "all_friends"),
    path("all_requests/", RequestView.as_view(), name = "all_requests"),
    path("recommended/", RecommendedView.as_view(), name = "recommended"),
    path("friend_profile/<int:friend_pk>", FriendProfileView.as_view(), name = "friend_profile"),
    path("delete_request/<int:pk>/", delete_request, name = "delete_request"),
    path("delete_recommened/<int:pk>", delete_recommended, name = "delete_recommended"),
    path("delete_friend/<int:pk>", delete_friend, name = "delete_friend"),
    path("confirm_friend/<int:pk>", confirm_friend, name = "confirm_friend"),
    path("sent_request/<int:pk>", request_to_user, name = "sent_request")
]
if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)