from django.contrib import admin
from django.urls import path, include
from kyc import views as kyc_views
from landing import views as landing_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # App URLs
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('kyc/', include('kyc.urls')),
    path('investments/', include('investments.urls')),

    # KYC custom paths
    path('submit/', kyc_views.submit_kyc, name='submit_kyc'),
    path('admin-view/', kyc_views.all_kyc_submissions, name='dashboard_admin_view'),
    path('kyc-submissions/', kyc_views.all_kyc_submissions, name='all_kyc_submissions'),

    # Landing page
    path('', landing_views.landing_page_view, name='index'),
]
