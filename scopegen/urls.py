from django.urls import path
from . import views

app_name = 'scopegen'

urlpatterns = [
    path('', views.scope_form_view, name='scope_form'),
    path('result/<int:pk>/', views.scope_result_view, name='scope_result'),
    path('download/<int:pk>/', views.scope_pdf_view, name='scope_pdf'),
    path('my/history/', views.scope_history_view, name='scope_history'),
    path('public/<uuid:uuid>/', views.scope_public_view, name='scope_public'),
    path('duplicate/<int:pk>/', views.duplicate_scope, name='scope_duplicate'),
    path('toggle-pitch/<int:pk>/', views.toggle_pitch_ready, name='toggle_pitch_ready'),
]
