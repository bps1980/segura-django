from django.db import models
from django.contrib.auth.models import User
from kyc.models import KYCSubmission


class Project(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField()
    whitepaper_url = models.URLField(blank=True, null=True)
    pitch_deck_url = models.URLField(blank=True, null=True)
    funding_min = models.DecimalField(max_digits=12, decimal_places=2)
    funding_max = models.DecimalField(max_digits=12, decimal_places=2)
    funding_goal = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)

    def __str__(self):
        return self.title

    def amount_raised(self):
        total = sum(investment.amount for investment in self.investments.all())
        return total

    def funding_progress_percent(self):
        if self.funding_goal > 0:
            return (self.amount_raised() / self.funding_goal) * 100
        return 0
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')

class InvestorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Investment(models.Model):
    PAYMENT_CHOICES = [
        ('stripe', 'Stripe'),
        ('plaid', 'Plaid'),
        ('crypto', 'Crypto'),
    ]

    investor = models.ForeignKey(InvestorProfile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='investments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.title} - {self.amount}"

class Payment(models.Model):
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=20)  # e.g. Stripe, Plaid, Crypto
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default='pending')  # pending, completed, failed
    created_at = models.DateTimeField(auto_now_add=True)
    plaid_payment_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.status}"

