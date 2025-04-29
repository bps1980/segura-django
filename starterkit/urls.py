"""
URL configuration for starterkit project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from kyc import views  # 👈 This is the missing piece
from . import views # 👈 This is the missing piece
from landing import views as landing_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('landing.urls')),  # 👈 this makes "/" go to your landing page
    path('accounts/', include('accounts.urls')),  # ← New auth routes
    path('dashboard/', include('dashboard.urls')),  # if you have one
    path('kyc/', include('kyc.urls')),
    path('submit', views.submit_kyc, name='submit_kyc'),  # 👈 This is the missing piece
    path('admin-view/', views.all_kyc_submissions, name='dashboard_admin_view'),
    path('', landing_views.landing_page_view, name='index'),
    path('kyc-submissions/', views.all_kyc_submissions, name='all_kyc_submissions'),
    path('investments/', include('investments.urls')),  # <-- use 'investments' here,
    path('index/', landing_views.landing_page_view, name='index'),  # optional, but good
]
