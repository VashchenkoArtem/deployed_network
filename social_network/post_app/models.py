from django.db import models
from user_app.models import Profile
# Create your models here.

#
class Post(models.Model):
    title = models.CharField(max_length = 255)
    content = models.TextField(max_length = 4096)
    author = models.ForeignKey(Profile, on_delete = models.CASCADE, null = True, blank = True)
    images = models.ManyToManyField("Image", blank = True, related_name = "posts_authored")
    views = models.ManyToManyField(Profile, blank = True, related_name = "posts_viewed")
    likes = models.ManyToManyField(Profile, blank = True, related_name = "posts_liked")
    tags = models.ManyToManyField("Tag", blank = True)
    topic = models.CharField(max_length=255)

    def __str__(self):
         return self.title

# 
class Image(models.Model):
    filename = models.CharField(max_length = 150)
    file = models.ImageField(upload_to = "images/posts")
    uploaded_at = models.DateTimeField(auto_now_add = True)
     
    def __str__(self):
        return self.filename

#
class Album(models.Model):
    name = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    preview_image = models.ImageField(upload_to = 'images/album_previews',null = True, blank = True)
    images = models.ManyToManyField(Image,blank = True)
    shown = models.BooleanField(default=  True)
    topic = models.ForeignKey("Tag", on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete = models.CASCADE)

    def __str__(self):
            return self.name
        
#
class Tag(models.Model):
    name = models.CharField(max_length = 50, unique = True)   
    def __str__(self):
        return self.name

#
class Link(models.Model):
    url = models.URLField(max_length = 200)
    post = models.ForeignKey(Post, on_delete = models.CASCADE) 
    def __str__(self):
        return f'Посилання для поста "{self.post}"'