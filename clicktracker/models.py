from django.db import models

class EmailLog(models.Model):
    company = models.CharField(max_length=255, blank=True)
    recipient_email = models.EmailField()
    country = models.CharField(max_length=100, blank=True)
    success = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)
    clicked = models.BooleanField(default=False)
    follow_up_sent = models.BooleanField(default=False)
    last_sent_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)