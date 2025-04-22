import requests, json, hmac, hashlib
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.conf import settings
from django.contrib.auth.decorators import login_required
from kyc.models import KYCSubmission
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import json
from .plaid_config import plaid_client
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from utils.decorators import twofa_required
import pprint
import os
from dotenv import load_dotenv

from .models import Project  # replace with your actual model name
from .models import Investment, Payment, Favorite
from investments.models import Favorite
from django.views.decorators.http import require_POST
# Set your Stripe secret key
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
@csrf_exempt
def toggle_favorite(request, project_id):
    project = Project.objects.get(id=project_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, project=project)

    if not created:
        favorite.delete()
        return JsonResponse({'status': 'removed'})
    else:
        return JsonResponse({'status': 'added'})

@login_required
def interested_projects(request):
    favorite_projects = Project.objects.filter(favorite__user=request.user)
    return render(request, 'dashboard/interested.html', {
        'projects': favorite_projects
    })

def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'investments/project_detail.html', {'project': project})

def dashboard_view(request):
    user_kyc = KYCSubmission.objects.filter(user=request.user).last()
    
    if not user_kyc or user_kyc.status != 'approved':
        return redirect('submit_kyc')
    
    # ...continue with dashboard logic
def segurainsures_whitepaper(request):
    return render(request, 'investments/segurainsures_whitepaper.html')

def segurainsures_pitch_deck(request): 
    return render(request, 'investments/segurainsures_pitch_deck.html')

def segurafinance_whitepaper(request):
    return render(request, 'investments/segurafinance_whitepaper.html')

def segurafinance_pitch_deck(request): 
    return render(request, 'investments/segurafinance_pitch_deck.html')    
    
def segurasafeswap_whitepaper(request):
    return render(request, 'investments/segurasafeswap_whitepaper.html')

def segurasafeswap_pitch_deck(request): 
    return render(request, 'investments/segurasafeswap_pitch_deck.html')

def cajunsea_whitepaper(request):
    return render(request, 'investments/cajunsea_whitepaper.html')

def cajunsea_pitch_deck(request): 
    return render(request, 'investments/cajunsea_pitch_deck.html')


def mdav_whitepaper(request):
    return render(request, 'investments/mdav_whitepaper.html')

def mdav_pitch_deck(request): 
    return render(request, 'investments/mdav_pitch_deck.html')


def dag_whitepaper(request):
    return render(request, 'investments/dag_whitepaper.html')

def dag_pitch_deck(request): 
    return render(request, 'investments/dag_pitch_deck.html')


def govtech_whitepaper(request):
    return render(request, 'investments/govtech_whitepaper.html')

def govtech_pitch_deck(request): 
    return render(request, 'investments/govtech_pitch_deck.html')

def hftbot_whitepaper(request):
    return render(request, 'investments/hftbot_whitepaper.html')

def hftbot_pitch_deck(request): 
    return render(request, 'investments/hftbot_pitch_deck.html')

def aichat_whitepaper(request):
    return render(request, 'investments/aichat_whitepaper.html')

def aichat_pitch_deck(request): 
    return render(request, 'investments/aichat_pitch_deck.html')

def arparks_whitepaper(request):
    return render(request, 'investments/arparks_whitepaper.html')

def arparks_pitch_deck(request): 
    return render(request, 'investments/arparks_pitch_deck.html')


def nga_whitepaper(request):
    return render(request, 'investments/nga_whitepaper.html')

def nga_pitch_deck(request): 
    return render(request, 'investments/nga_pitch_deck.html')


def xactimate_whitepaper(request):
    return render(request, 'investments/xactimate_whitepaper.html')

def xactimate_pitch_deck(request): 
    return render(request, 'investments/xactimate_pitch_deck.html')

def sam_whitepaper(request):
    return render(request, 'investments/sam_whitepaper.html')

def sam_pitch_deck(request): 
    return render(request, 'investments/sam_pitch_deck.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('onboarding')  # or wherever you want to send them
    else:
        form = UserCreationForm()
    return render(request, 'auth/signupbasic.html', {'form': form})


# ✅ Stripe checkout view
@login_required
def stripe_checkout(request, investment_id):
    investment = get_object_or_404(Investment, id=investment_id)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': f"Investment in {investment.project}",
                },
                'unit_amount': int(investment.amount * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/payments/success/'),
        cancel_url=request.build_absolute_uri('/payments/cancel/'),
    )

    # Track payment in database
    Payment.objects.create(
        investment=investment,
        payment_type='stripe',
        amount=investment.amount,
        transaction_id=session.id,
        status='pending'
    )

    return redirect(session.url, code=303)


# ✅ Payment success + cancel views
@login_required
def payment_success(request):
    return render(request, 'payments/success.html')

@login_required
def payment_cancel(request):
    return render(request, 'payments/cancel.html')

@login_required
def onboarding(request):
    return render(request, 'auth/onboarding.html')  # Update path if needed

def home(request):
    investments = Investment.objects.all()
    return render(request, 'landing/index.html', {'investments': investments})

@csrf_exempt
def set_access_token(request):
    data = json.loads(request.body)
    public_token = data['public_token']
    
    exchange_response = plaid_client.Item.public_token.exchange(public_token)
    access_token = exchange_response['access_token']

    # Save access_token to user/investor profile or secure storage

    return JsonResponse({'status': 'success'})

@login_required
def create_link_token(request):
    try:
        user_id = str(request.user.id)
        if not user_id:
            raise ValueError("User ID is missing or invalid.")

        request_data = LinkTokenCreateRequest(
            user=LinkTokenCreateRequestUser(client_user_id=user_id),
            client_name='Segura Investments',
            products=[Products("auth")],
            country_codes=[CountryCode("US")],
            language='en',
        )

        # Optional debug output
        pprint.pprint(request_data.to_dict())

        response = plaid_client.link_token_create(request_data)
        return JsonResponse(response.to_dict())

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
def create_coinbase_charge(request):
    if request.method == 'POST':
        headers = {
            "X-CC-Api-Key": os.getenv("COINBASE_COMMERCE_API_KEY"),
            "X-CC-Version": "2018-03-22",
            "Content-Type": "application/json"
        }

        data = {
            "name": "Segura Premium Access",
            "description": "Full access to Segura services",
            "pricing_type": "fixed_price",
            "local_price": {
                "amount": "50.00",
                "currency": "USD"
            }
        }

        response = requests.post("https://api.commerce.coinbase.com/charges", json=data, headers=headers)

        if response.status_code == 201:
            hosted_url = response.json()['data']['hosted_url']
            return redirect(hosted_url)
        else:
            return HttpResponse("Error creating charge", status=500)

    return render(request, 'payments/pay.html')

@csrf_exempt
def coinbase_webhook(request):
    request_sig = request.headers.get("X-CC-Webhook-Signature", "")
    webhook_secret = "your_webhook_shared_secret"

    computed_sig = hmac.new(
        webhook_secret.encode(),
        request.body,
        hashlib.sha256
    ).hexdigest()

    if hmac.compare_digest(computed_sig, request_sig):
        event = json.loads(request.body)
        if event['event']['type'] == 'charge:confirmed':
            print("✅ Payment confirmed:", event['event']['data']['code'])
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'invalid'}, status=400)

def dashboard(request):
    projects = Project.objects.all()
    user_favorites = Favorite.objects.filter(user=request.user).values_list('project_id', flat=True)
    return render(request, 'dashboard/index.html', {
        'projects': projects,
        'user_favorites': list(user_favorites),  # convert to list for template usage
    })

@login_required
@twofa_required
def stripe_checkout(request, investment_id):
    # Only allow if user has passed 2FA
    ...

@require_POST
@login_required
def create_investment_then_stripe(request):
    data = json.loads(request.body)
    amount = data.get("amount")
    project_id = data.get("project_id")

    if not amount or not project_id:
        return JsonResponse({"error": "Missing amount or project ID"}, status=400)

    try:
        project = Project.objects.get(id=project_id)
        profile, _ = InvestorProfile.objects.get_or_create(user=request.user)

        investment = Investment.objects.create(
            investor=profile,
            project=project,
            amount=amount,
            payment_method="stripe"  # You can make this dynamic later if needed
        )

        return JsonResponse({
            "redirect_url": f"/investments/stripe/checkout/{investment.id}/"
        })

    except Project.DoesNotExist:
        return JsonResponse({"error": "Project not found"}, status=404)