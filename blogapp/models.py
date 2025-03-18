from django.db import models
from django.contrib.auth.models import User


class blog_listmodel(models.Model):
    title = models.CharField(max_length=100)  
    content = models.TextField()  
    travel_photos = models.ImageField(upload_to='travel_photos/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs', null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pic/', default='default.jpg')
    
    def __str__(self):
        return f'{self.user.username} Profile'
    




