# kyc/context_processors.py

from .models import KYCSubmission

def inject_kyc_status(request):
    if request.user.is_authenticated:
        submission = KYCSubmission.objects.filter(user=request.user).order_by('-submitted_at').first()
        if submission:
            return {'kyc_status': submission.status}
    return {'kyc_status': 'not_started'}
