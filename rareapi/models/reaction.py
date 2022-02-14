from django.db import models

class Reaction(models.Model):
    label = models.CharField(max_length=9999)
    image_url = models.ImageField(null=True)