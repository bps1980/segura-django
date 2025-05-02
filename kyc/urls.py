# urls.py
from django.urls import path
from .views import start_veriff_session
from .views import veriff_callback
from . import views
from .views import kyc_status_view


urlpatterns = [
    path('start-veriff/', start_veriff_session, name='start_veriff'),
    path('webhook/veriff/', veriff_callback, name='veriff_callback'),
    path('status/', kyc_status_view, name='kyc_status'),
    path('kyc-required/', views.kyc_required_notice, name='kyc_required_notice'),
    path('submit/', views.submit_kyc, name='submit_kyc'),
]
