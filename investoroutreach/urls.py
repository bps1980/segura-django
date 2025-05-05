from django.urls import path
from . import views

app_name = 'investoroutreach'

urlpatterns = [
    path('upload/', views.upload_excel, name='upload_excel'),
    path('send/', views.send_emails, name='send_emails'),
    path('import-local/', views.load_from_disk, name='load_from_disk'),

]
