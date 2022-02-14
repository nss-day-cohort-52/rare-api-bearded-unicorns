from django.db import models

class Comment(models.Model):
    post_id = models.ForeignKey("Post", on_delete=models.CASCADE)
    author_id = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)