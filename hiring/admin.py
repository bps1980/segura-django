from django.contrib import admin
from .models import JobApplication

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'scope', 'submitted_at')  # ✅ match field names
    search_fields = ('name', 'email', 'scope__project_type')
    list_filter = ('submitted_at',)
