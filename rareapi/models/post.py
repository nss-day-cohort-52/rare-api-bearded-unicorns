from django.db import models



class Post(models.Model):
    title = models.CharField(max_length=9999)
    publication_date = models.DateField(auto_now_add=True)
    image_url = models.ImageField(null=True)
    content = models.TextField()
    approved = models.BooleanField(default=True)
    user = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag", through="PostTag")
