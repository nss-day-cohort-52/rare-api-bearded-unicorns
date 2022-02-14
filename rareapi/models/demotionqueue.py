from django.db import models

class DemotionQueue(models.Model):
    action = models.CharField(max_length=9999)
    admin_id = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="admin")
    approver_one_id = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="approver")
