from django.contrib import admin
from post_app.models import Tag, Post
# Register your models here.


admin.site.register([Tag, Post])