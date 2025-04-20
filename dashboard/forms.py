# certificates/forms.py
from django import forms
from .models import Certificate

class CertificateForm(forms.Form):
    investor_name = forms.CharField(max_length=255)
    certificate_id = forms.CharField(max_length=100)
    date_issued = forms.DateField()  # ✅ Not "investment_date"
    signature = forms.ImageField(required=False)
