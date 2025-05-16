from django.contrib import admin
from .models import ScopeOfWork
from .views import generate_scope  # reuse your existing function

class ScopeOfWorkAdmin(admin.ModelAdmin):
    list_display = ("project_type", "industry", "user", "created_at")
    readonly_fields = ("generated_scope", "share_uuid", "created_at")

    def save_model(self, request, obj, form, change):
        if not obj.generated_scope:
            prompt = f"""Create a professional Scope of Work for a {obj.get_category_display()} project:
- Project Type: {obj.project_type}
- Industry: {obj.industry}
- Goals: {obj.goals}
- Tools: {obj.tools}
- Timeline: {obj.timeline}
"""
            obj.generated_scope = generate_scope(prompt)
        super().save_model(request, obj, form, change)

# ✅ Only this one registration call:
admin.site.register(ScopeOfWork, ScopeOfWorkAdmin)