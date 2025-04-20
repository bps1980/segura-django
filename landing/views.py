from django.shortcuts import render
from investments.models import Project, Favorite

def landing_page_view(request):
    projects = Project.objects.all()
    return render(request, 'landing/index.html', {'projects': projects})

def dashboard(request):
    projects = Project.objects.all()
    user_favorites = Favorite.objects.filter(user=request.user).values_list('project_id', flat=True)
    return render(request, 'dashboard/index.html', {
        'projects': projects,
        'user_favorites': list(user_favorites),  # convert to list for template usage
    })