from django.contrib import admin
from user_app.models import Avatar, VerificationCode
# Register your models here.


admin.site.register([Avatar, VerificationCode])