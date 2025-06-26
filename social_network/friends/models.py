from django.contrib import admin
from user_app.models import Profile, Friendship

# Register your models here.

admin.site.register(Profile)
admin.site.register(Friendship)