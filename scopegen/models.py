# scopegen/models.py
import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ScopeTag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class ScopeOfWork(models.Model):
    CATEGORY_CHOICES = [
        ('ai', 'AI/ML'),
        ('blockchain', 'Blockchain'),
        ('web', 'Web Dev'),
        ('mobile', 'Mobile App'),
        ('data', 'Data Science'),
        ('general', 'General')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_type = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    goals = models.TextField()
    tools = models.CharField(max_length=255)
    timeline = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    tags = models.ManyToManyField(ScopeTag, blank=True)
    generated_scope = models.TextField(blank=True)
    share_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    is_shared = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_pitch_ready = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project_type} - {self.user.email}"

    class Meta:
        ordering = ['-created_at']
