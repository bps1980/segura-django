from django.shortcuts import redirect
from kyc.models import KYCSubmission
from functools import wraps

def kyc_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        latest_kyc = KYCSubmission.objects.filter(user=request.user).last()
        if not latest_kyc or latest_kyc.status != 'approved':
            return redirect('start_veriff')  # 👈 URL name for your Veriff launch view
        return view_func(request, *args, **kwargs)
    return wrapper
