from django.db import models
from user_app.models import Profile


class ChatGroup(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(Profile, blank=True)
    is_personal_chat = models.BooleanField(default=False)
    admin = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name= "adminstered_group")
    avatar = models.ImageField(upload_to="images/group_avatars", blank = True, null = True)
    def __str__(self):
        return f'Група "{self.name}" '
    

class ChatMessage(models.Model):
    content = models.TextField(max_length=4096)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    chat_group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    attached_image = models.ImageField(upload_to='images/messages', blank = True, null = True)

    def __str__(self):
        return f'Повідомлення від "{self.author}. Відправлено {self.sent_at} '
    