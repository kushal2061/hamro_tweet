from django.db import models
from django.contrib.auth.models import User

class Tweet(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    text= models.TextField(max_length=250)
    photo= models.ImageField( upload_to="photos/", blank=True , null=True)
    created_at=models.DateTimeField( auto_now_add=True)
    updated_at=models.DateTimeField( auto_now=True)

    def __str__(self):
        return f"{self.user.username} -{self.text[:10]} "
    

class Profile(models.Model):
    user =models.OneToOneField(User,on_delete=models.CASCADE)
    p_img=models.ImageField(upload_to="photos/" ,default='media/photos/default_profile.jpg', blank=True,null=True)
    dob= models.DateField(null=True, blank=True)
    country=models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}-{self.user.first_name}"

