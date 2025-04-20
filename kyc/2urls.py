from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_kyc, name='submit_kyc'),
    path('status/', views.kyc_status, name='kyc_status'),
]
