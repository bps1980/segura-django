from django.contrib import admin
from .models import InvestorProfile, Investment, Payment, Project

@admin.register(InvestorProfile)
class InvestorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'phone']

@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ['investor', 'project', 'amount', 'payment_method', 'created_at']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['investment', 'payment_type', 'amount', 'transaction_id', 'status', 'created_at']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'funding_min', 'funding_max']