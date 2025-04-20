from django import forms
from .models import KYCSubmission

class KYCSubmissionForm(forms.ModelForm):
    class Meta:
        model = KYCSubmission
        fields = ['full_name', 'date_of_birth', 'address', 'id_document', 'selfie']
