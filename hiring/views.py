from django.shortcuts import render, get_object_or_404, redirect
from scopegen.models import ScopeOfWork
from .models import JobApplication
from .forms import JobApplicationForm

def hiring_landing(request):
    scopes = ScopeOfWork.objects.filter(is_hiring=True, is_shared=True, is_approved=True)
    return render(request, 'hiring/landing.html', {'scopes': scopes})

def scope_detail(request, uuid):
    scope = get_object_or_404(ScopeOfWork, share_uuid=uuid, is_hiring=True, is_shared=True, is_approved=True)
    return render(request, 'hiring/scope_detail.html', {'scope': scope})

def apply_to_scope(request, uuid):
    scope = get_object_or_404(ScopeOfWork, share_uuid=uuid, is_hiring=True)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.scope = scope
            application.save()
            return redirect('hiring:application_success')
    else:
        form = JobApplicationForm()
    return render(request, 'hiring/apply.html', {'form': form, 'scope': scope})

def application_success(request):
    return render(request, 'hiring/success.html')
