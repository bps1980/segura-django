from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import KYCSubmission

@admin.register(KYCSubmission)
class KYCSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'submitted_at', 'reviewed_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'full_name')
