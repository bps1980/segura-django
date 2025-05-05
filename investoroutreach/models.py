from django.db import models

class EmailLog(models.Model):
    company = models.CharField(max_length=255, blank=True)
    recipient_email = models.EmailField()
    country = models.CharField(max_length=100, blank=True)
    success = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company} – {self.recipient_email} – {'Success' if self.success else 'Failed'}"

class Investor(models.Model):
    company_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    second_email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True)
    investor_type = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=255, blank=True)
    employees = models.CharField(max_length=100, blank=True)
    number_of_investments = models.IntegerField(null=True, blank=True)
    number_of_exits = models.IntegerField(null=True, blank=True)
    domain = models.CharField(max_length=255, blank=True)
    industries = models.TextField(blank=True)
    key_people = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name or "Investor"