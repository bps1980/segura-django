from django.urls import path
from . import views

app_name = 'clicktracker'

urlpatterns = [
    path('click/<int:investor_id>/', views.email_clicked, name='email_clicked'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('review/<int:log_id>/', views.mark_reviewed, name='mark_reviewed'),
]