from django import forms
from .models import InvestorProfile

class InvestorProfileForm(forms.ModelForm):
    class Meta:
        model = InvestorProfile
        fields = ['company', 'phone', 'address']
