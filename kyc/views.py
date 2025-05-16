import uuid
import time
import requests
import json
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import KYCSubmission
from dashboard.models import Notification
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
from django.http import JsonResponse, HttpResponseBadRequest
import json

load_dotenv()

@csrf_exempt
@login_required
def start_veriff_session(request):
    try:
        base_url = os.getenv("VERIFF_BASE_URL")
        api_key = os.getenv("VERIFF_API_KEY")
        api_secret = os.getenv("VERIFF_API_SECRET")
        
        print("🔍 Veriff Base URL:", base_url)
        print("🔍 API Key present:", bool(api_key))
        print("🔍 API Secret present:", bool(api_secret))

        if not base_url or not api_key or not api_secret:
            raise Exception("Missing Veriff environment variables.")

        payload = {
            "verification": {
                "callback": "https://app.seguramgmt.com/kyc/status/",
                "vendorData": str(request.user.id),
                "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "document": {
                    "type": "ID_CARD"
                }
            }
        }

        headers = {
            "X-AUTH-CLIENT": api_key,
            "Content-Type": "application/json"
        }

        response = requests.post(f"{base_url}/v1/sessions", headers=headers, json=payload)
        print("📬 Veriff API Response:", response.status_code, response.text)

        if response.status_code == 201:
            data = response.json()
            session_id = data['verification']['id']
            session_url = data['verification']['url']

            KYCSubmission.objects.create(
                session_id=session_id,
                user=request.user,
                full_name=f"{request.user.first_name} {request.user.last_name}",
                date_of_birth="2000-01-01",
                address="TBD",
                status="pending"
            )

            return redirect(session_url)

        else:
            return render(request, 'kyc/error.html', {
                "error_message": f"Status: {response.status_code}\nBody: {response.text}"
            })

    except Exception as e:
        print("💥 Exception occurred:", str(e))
        return render(request, 'kyc/error.html', {"error_message": str(e)})

@csrf_exempt
def veriff_webhook(request):
    print(f"➡️ Method: {request.method}")
    print(f"➡️ Path: {request.path}")
    print(f"➡️ Headers: {dict(request.headers)}")  # This will show the Referer and User-Agent

    if request.method != 'POST':
        print("❌ GET or unsupported method received at webhook")
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
        print("✅ Webhook POST received:", data)
        return JsonResponse({"status": "received"})
    except Exception as e:
        print("❌ Error parsing webhook:", e)
        return HttpResponseBadRequest("Invalid JSON")


@login_required
def kyc_status_view(request):
    try:
        kyc = KYCSubmission.objects.filter(user=request.user).latest('submitted_at')
        kyc_status = kyc.status
    except KYCSubmission.DoesNotExist:
        kyc = None
        kyc_status = "not_started"

    return render(request, 'kyc/status.html', {
        'kyc': kyc,
        'kyc_status': kyc_status,
    })


def all_kyc_submissions(request):
    submissions = KYCSubmission.objects.all().order_by('-submitted_at')
    return render(request, 'kyc/all_kyc_submissions.html', {'submissions': submissions})


def kyc_required_notice(request):
    return render(request, 'kyc/required_notice.html')


def submit_kyc(request):
    return render(request, 'kyc/submit_kyc.html')
