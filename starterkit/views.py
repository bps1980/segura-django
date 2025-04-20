from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import KYCSubmission
from django.shortcuts import render


@staff_member_required
def all_kyc_submissions(request):
    submissions = KYCSubmission.objects.select_related('user').order_by('-submitted_at')
    return render(request, 'kyc/all_kyc_submissions.html', {'submissions': submissions})
