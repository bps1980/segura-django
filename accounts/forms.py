# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class OnboardingForm(forms.Form):
    full_name = forms.CharField()
    phone = forms.CharField()
    address = forms.CharField()
    country = forms.CharField()
    accredited = forms.BooleanField(required=False)
    wallet_address = forms.CharField(required=False)
    
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
class TwoFactorCodeForm(forms.Form):
    code = forms.CharField(max_length=4, min_length=4, widget=forms.TextInput(attrs={'autocomplete': 'off'}))