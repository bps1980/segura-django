from django.test import TestCase

# Create your tests here.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class KYCSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    address = models.TextField()
    
    id_document = models.ImageField(upload_to='kyc_uploads/id_docs/')
    selfie = models.ImageField(upload_to='kyc_uploads/selfies/')
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'KYC for {self.user.username} - {self.status}'
