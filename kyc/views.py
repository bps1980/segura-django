# views.py
import uuid
import time
import hashlib
import hmac
import requests
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import KYCSubmission  # ✅ Your model
from datetime import datetime, timezone
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

@csrf_exempt
@login_required
def start_veriff_session(request):
    try:
        base_url = os.getenv("VERIFF_BASE_URL")
        api_key = os.getenv("VERIFF_API_KEY")
        api_secret = os.getenv("VERIFF_API_SECRET")

        print("🔍 Veriff ENV Check:")
        print("BASE URL:", base_url)
        print("API KEY:", api_key)
        print("API SECRET exists:", bool(api_secret))

        if not base_url or not api_key or not api_secret:
            raise Exception("Missing Veriff environment variables.")

        # Minimal payload without timestamp & nonce
        payload = {
            "verification": {
                "callback": "https://www.veriff.com/get-verified?navigation=slim/kyc/veriff_callback",
                "person": {
                    "firstName": request.user.first_name or "John",
                    "lastName": request.user.last_name or "Doe"
                },
                "vendorData": f"user-{request.user.id}"
            }
        }

        headers = {
            "X-AUTH-CLIENT": api_key,
            "Content-Type": "application/json"
            # 🔥 Remove X-HMAC-SIGNATURE unless HMAC is enabled in Veriff dashboard
        }

        print("📤 Sending request to:", f"{base_url}/v1/sessions")
        print("📦 Payload:", json.dumps(payload))

        # Use `json=` so headers are respected
        response = requests.post(f"{base_url}/v1/sessions", headers=headers, json=payload)

        print("📥 Veriff response:", response.status_code, response.text)

        if response.status_code == 201:
            session_url = response.json()['verification']['url']
            return redirect(session_url)
        else:
            return render(request, 'kyc/error.html', {"error_message": response.text})

    except Exception as e:
        print("💥 Exception occurred:", str(e))
        return render(request, 'kyc/error.html', {"error_message": str(e)})

@csrf_exempt
def veriff_callback(request):
    data = json.loads(request.body)
    print("🔄 Veriff callback received:", data)

    try:
        session_id = data['verification']['id']
        status = data['verification']['status']

        KYCSubmission.objects.filter(session_id=session_id).update(status=status)
        print(f"✅ KYC status updated for session {session_id} to {status}")

    except Exception as e:
        print(f"❌ Error processing Veriff webhook: {e}")
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "received"})

def all_kyc_submissions(request):
    submissions = KYCSubmission.objects.all().order_by('-submitted_at')
    return render(request, 'kyc/all_kyc_submissions.html', {'submissions': submissions})

def kyc_required_notice(request):
    return render(request, 'kyc/required_notice.html')

def submit_kyc(request):
    return render(request, 'kyc/submit_kyc.html')