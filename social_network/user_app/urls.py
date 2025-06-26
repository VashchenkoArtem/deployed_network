from django.contrib import admin
from django.urls import path
from .views import *
from social_network.settings import MEDIA_URL, MEDIA_ROOT, DEBUG
from django.conf.urls.static import static


urlpatterns = [
    path("registration/", RegistrationView.as_view(), name = "registration"),
    path("confirm/", ConfirmRegistrationView.as_view(), name = "confirm"),
    path("authorithation/", AuthorizationView.as_view(), name = "authorithation")
]
if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)