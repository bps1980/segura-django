from django.contrib import admin
from .models import EmailLog, Investor

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('company', 'recipient_email', 'country', 'success', 'reviewed', 'created_at')
    list_filter = ('success', 'reviewed', 'country')
    search_fields = ('company', 'recipient_email', 'country')
    actions = ['mark_as_reviewed']

    def mark_as_reviewed(self, request, queryset):
        queryset.update(reviewed=True)
    mark_as_reviewed.short_description = "Mark selected emails as reviewed"

@admin.register(Investor)
class InvestorAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'email', 'country', 'investor_type', 'created_at')
    list_filter = ('country', 'investor_type')
    search_fields = ('company_name', 'email')