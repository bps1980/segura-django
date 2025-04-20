# urls.py
from django.urls import path
from .views import start_veriff_session
from .views import veriff_callback
from . import views


urlpatterns = [
    path('start-veriff/', start_veriff_session, name='start_veriff'),
    path('webhook/veriff/', veriff_callback, name='veriff_callback'),
    path('kyc-required/', views.kyc_required_notice, name='kyc_required_notice'),
]
