from django.contrib import admin
from .models import ChatGroup, ChatMessage
# Register your models here.


admin.site.register([ChatGroup, ChatMessage])