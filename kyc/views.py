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

        if not base_url or not api_key or not api_secret:
            raise Exception("Missing Veriff environment variables.")

        payload = {
            "verification": {
                "callback": "https://segura-django-1.onrender.com/kyc/webhook/veriff/",
                "person": {
                    "firstName": request.user.first_name or "John",
                    "lastName": request.user.last_name or "Doe"
                },
                "vendorData": f"user-{request.user.id}",
                "timestamp": int(time.time()),  # Veriff may require this
                "lang": "en",
                "successUrl": "https://segura-django-1.onrender.com/dashboard/",
                "errorUrl": "https://segura-django-1.onrender.com/kyc/error/"
            }
        }

        headers = {
            "X-AUTH-CLIENT": api_key,
            "Content-Type": "application/json"
        }

        response = requests.post(f"{base_url}/v1/sessions", headers=headers, json=payload)
        data = response.json()

        if response.status_code == 201:
            session_id = data['verification']['id']
            session_url = data['verification']['url']

            # Save initial KYCSubmission record
            KYCSubmission.objects.create(
                session_id=session_id,
                user=request.user,
                full_name=f"{request.user.first_name} {request.user.last_name}",
                date_of_birth="2000-01-01",  # You can update later
                address="TBD",
                status="pending"
            )

            return redirect(session_url)

        else:
            return render(request, 'kyc/error.html', {"error_message": response.text})

    except Exception as e:
        print("💥 Exception occurred:", str(e))
        return render(request, 'kyc/error.html', {"error_message": str(e)})


from dashboard.models import Notification  # ✅ Import if not already

@csrf_exempt
def veriff_callback(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Invalid method"}, status=405)

    try:
        data = json.loads(request.body)
        print("🔄 Veriff callback received:", data)

        session_id = data['verification']['id']
        status = data['verification']['status']

        submission = KYCSubmission.objects.filter(session_id=session_id).first()
        if submission:
            submission.status = status
            submission.reviewed_at = datetime.now(timezone.utc)
            submission.save()

            # ✅ Create in-app notification
            Notification.objects.create(
                user=submission.user,
                message=f"KYC verification {status.capitalize()}",
                link="/dashboard/"
            )

            print(f"✅ KYC status updated for session {session_id} to {status}")
        else:
            print(f"⚠️ No KYCSubmission found for session {session_id}")

        return JsonResponse({"status": "received"})

    except Exception as e:
        print(f"❌ Error processing Veriff webhook: {e}")
        return JsonResponse({"status": "error", "message": str(e)}, status=400)


@login_required
def kyc_status_view(request):
    try:
        kyc = KYCSubmission.objects.filter(user=request.user).latest('submitted_at')
        kyc_status = kyc.status if kyc else None
    except KYCSubmission.DoesNotExist:
        kyc = None

    return render(request, 'kyc/status.html', {'kyc': kyc})

def all_kyc_submissions(request):
    submissions = KYCSubmission.objects.all().order_by('-submitted_at')
    return render(request, 'kyc/all_kyc_submissions.html', {'submissions': submissions})

def kyc_required_notice(request):
    return render(request, 'kyc/required_notice.html')

def submit_kyc(request):
    return render(request, 'kyc/submit_kyc.html')