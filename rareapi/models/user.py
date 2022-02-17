from django.db import models
from django.contrib.auth.models import User

class RareUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=9999)
    profile_image_url= models.ImageField(upload_to='actionimages', height_field=None,
        width_field=None, max_length=None, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    