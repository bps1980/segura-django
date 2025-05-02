# certificates/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    link = models.URLField(blank=True, null=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To {self.user.username}: {self.message[:30]}"


class Certificate(models.Model):
    investor_name = models.CharField(max_length=255)
    certificate_id = models.CharField(max_length=50)
    date_issued = models.DateField()
    signature = models.ImageField(upload_to='signatures/')
    pdf_file = models.FileField(upload_to='certificates/', blank=True)

class Investment(models.Model):
    agreement_signed = models.BooleanField(default=False)
    agreement_signed_at = models.DateTimeField(null=True, blank=True)