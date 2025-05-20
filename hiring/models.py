from django.db import models

# Create your models here.
from django.db import models
from scopegen.models import ScopeOfWork

class JobApplication(models.Model):
    scope = models.ForeignKey(ScopeOfWork, on_delete=models.CASCADE, related_name='applications')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} – {self.scope.project_type}"
