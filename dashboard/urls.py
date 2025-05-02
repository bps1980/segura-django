from . import views
from django.urls import path
from .views import generate_certificate_view, interested_projects_view, profile_view, help_view, notifications_view  # ✅ Add this

appname = 'dashboard'

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('dashboard', views.index, name='dashboard'),
    path('settings/', views.account_settings, name='settings'),
    path('profile/', views.profile_view, name='profile'),
    path('help/', views.help_view, name='help'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('invested/', views.invested_projects, name='invested_projects'),
    path('interested/', interested_projects_view, name='interested_projects'),  # ✅ Fix here
    path('payments/', views.investment_payments, name='investment_payments'),

    # Files
    path('files/agreements/', views.investment_agreements, name='investment_agreements'),
    path('files/receipts/', views.investment_receipts, name='investment_receipts'),
    path('files/certificates/', views.investor_certificates, name='investor_certificates'),
    path('generate-certificate/', generate_certificate_view, name='generate_certificate'),
    path('files/regulatory/', views.regulatory_docs, name='regulatory_docs'),

    path('kyc/', views.kyc_list, name='kyc_list'),
    
    path('employee/', views.employee_view, name='employee_home'),
    path('admin-dashboard/', views.admin_view, name='admin_dashboard'),
    path('test-protected/', views.test_protected_view, name='test_protected'),
    path('', views.index, name='dashboard_home'),  # ✅ Add this name
]