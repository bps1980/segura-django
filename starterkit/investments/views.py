from utils.decorators import kyc_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


@login_required
@kyc_required
def stripe_checkout(request, investment_id):
    ...

@login_required
@kyc_required
@csrf_exempt
def set_access_token(request):
    ...

@login_required
@kyc_required
@csrf_exempt
def create_coinbase_charge(request):
    ...
