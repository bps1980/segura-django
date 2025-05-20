from django.urls import path
from . import views

app_name = 'hiring'

urlpatterns = [
    path('', views.hiring_landing, name='landing'),
    path('scope/<uuid:uuid>/', views.scope_detail, name='scope_detail'),
    path('apply/<uuid:uuid>/', views.apply_to_scope, name='apply'),
    path('success/', views.application_success, name='application_success'),
]
