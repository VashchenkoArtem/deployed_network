from django.db import models
from django.contrib.auth.models import AbstractBaseUser, User
from django.contrib.auth import get_user_model
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null = True)   
    signature = models.ImageField(upload_to="images/signatures", blank = True, null = True)

    def __str__(self):
        return self.user.username
class Avatar(models.Model):
    image = models.ImageField(upload_to = "images/avatars")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    active = models.BooleanField(default = True)
    shown = models.BooleanField(default = True)
    def __str__(self):
        return f'Аватар для профілю {self.profile}'

class Friendship(models.Model):
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="friendship_sent_request") # Той, хто надсилає запит
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="friendship_accepted_request") # Той, хто приймає запит
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'Дружба між {self.profile1} та {self.profile2}'
    
class VerificationCode(models.Model):
    username = models.CharField(max_length=150)
    code = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
# class RequestModel(models.Model):
#     sent_user = models.ForeignKey(User,related_name = "sent_request", on_delete=models.CASCADE, null = True)
#     received_user = models.ForeignKey(User,related_name = "received_request", on_delete=models.CASCADE, null = True)
#     is_friend = models.BooleanField(default=False)
    

    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    # date_of_birth = models.DateField(auto_now_add=True)
    # profile_image = models.ImageField(upload_to= "images/profile_images/",default = "/../images/account.png", blank = True)
    # friends = models.ManyToManyField('self', related_name = "friends", symmetrical=True, blank = True)
    # requests = models.ManyToManyField(RequestModel, related_name = "requests", blank = True)
    # def remove_friend(self, friend):
        
    #     if friend in self.friends.all():
    #         self.friends.remove(friend)
    #         friend.friends.remove(self)
    # def __str__(self):
    #     return f'{self.user}'
