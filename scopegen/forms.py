# scopegen/forms.py
from django import forms
from .models import ScopeOfWork

class ScopeOfWorkForm(forms.ModelForm):
    class Meta:
        model = ScopeOfWork
        fields = ['project_type', 'industry', 'goals', 'tools', 'timeline', 'category']
        widgets = {
            'goals': forms.Textarea(attrs={'rows': 4}),
        }
