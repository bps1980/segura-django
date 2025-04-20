# signals.py in investments app
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import InvestorProfile
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_investor_profile(sender, instance, created, **kwargs):
    if created:
        InvestorProfile.objects.create(user=instance)
