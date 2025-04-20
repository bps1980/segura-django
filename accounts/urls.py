from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import account_settings, custom_login_view

urlpatterns = [
    path('login/', custom_login_view, name='login'),  # ✅ Use your custom login flow
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('onboarding/', views.onboarding, name='onboarding'),
    path('settings/', account_settings, name='account_settings'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='dashboard/change_password.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='dashboard/change_password_done.html'), name='password_change_done'),
    path('2fa/send/', views.send_2fa_code, name='send_2fa_code'),
    path('2fa/verify/', views.twofactor_verify, name='twofactor_verify'),
]