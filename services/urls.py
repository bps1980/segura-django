from django.urls import path
from . import views

urlpatterns = [
    path("quick-dev/", views.quick_dev_service, name="quick_dev_service"),
]
