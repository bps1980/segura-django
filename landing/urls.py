from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page_view, name='index'),  # <-- Use this view
]
