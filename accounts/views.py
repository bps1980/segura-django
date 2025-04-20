from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail
from django.utils import timezone
import random, datetime
from .forms import CustomUserCreationForm as UserCreationForm
from django.conf import settings


from .forms import TwoFactorCodeForm, OnboardingForm, UserUpdateForm
from utils.tokens import email_verification_token


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']  # ⬅️ Save the email properly
            user.is_active = False  # Wait for email verification
            user.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = email_verification_token.make_token(user)

            verification_url = request.build_absolute_uri(
                f"/accounts/verify/{uid}/{token}/"
            )

            subject = "Verify your email address"
            message = render_to_string("accounts/verify_email.html", {
                'user': user,
                'verification_url': verification_url,
            })

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

            return render(request, 'accounts/email_verification_sent.html')
    else:
        form = CustomUserCreationForm()

    return render(request, 'auth/signupbasic.html', {'form': form})


# ✅ EMAIL Verification → Login → Redirect to 2FA
def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)  # ✅ Log in user
        return redirect('send_2fa_code')  # 🚀 Trigger 2FA
    else:
        return HttpResponse("❌ Invalid or expired verification link.")


# ✅ LOGIN with 2FA trigger
def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('send_2fa_code')  # 🔐 Send code
    else:
        form = AuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})


# ✅ 2FA Code Sender
@login_required
def send_2fa_code(request):
    if not request.user.is_authenticated:
        return redirect('login')

    code = str(random.randint(1000, 9999))
    request.session['2fa_code'] = code
    request.session['2fa_code_expiry'] = (
        timezone.now() + datetime.timedelta(minutes=5)
    ).isoformat()

    print("🔐 Generated 2FA code:", code)
    print("📧 Sending to:", request.user.email)
    print("📧 EMAIL USER FROM SETTINGS:", settings.EMAIL_HOST_USER)


    send_mail(
        "Your 2FA Code",
        f"Your verification code is: {code}",
        settings.DEFAULT_FROM_EMAIL,
        [request.user.email],
    )

    print("✅ Email send_mail() function executed.")
    print("📧 Sending to:", request.user.email)

    return redirect('twofactor_verify')

# ✅ 2FA Code Verifier
@login_required
def twofactor_verify(request):
    form = TwoFactorCodeForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        submitted_code = form.cleaned_data['code']
        stored_code = request.session.get('2fa_code')
        expiry_str = request.session.get('2fa_code_expiry')

        if not stored_code or not expiry_str:
            messages.error(request, "Code expired or not found.")
            return redirect('send_2fa_code')

        expiry = datetime.datetime.fromisoformat(expiry_str)
        if timezone.now() > expiry:
            messages.error(request, "Code has expired.")
            return redirect('send_2fa_code')

        if submitted_code == stored_code:
            # ✅ Mark session as 2FA passed
            request.session['2fa_passed'] = True
            del request.session['2fa_code']
            del request.session['2fa_code_expiry']
            return redirect('dashboard_home')  # ✅ Customize this as needed
        else:
            messages.error(request, "Invalid code.")

    return render(request, 'accounts/twofactor_code.html', {'form': form})


# ✅ ACCOUNT SETTINGS UPDATE
@login_required
def account_settings(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Account details updated successfully.")
            return redirect('account_settings')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'dashboard/settings.html', {'form': form})

@login_required
def onboarding(request):
    if request.method == 'POST':
        form = OnboardingForm(request.POST)
        if form.is_valid():
            # Save or process onboarding data
            return redirect('dashboard_home')  # or wherever
    else:
        form = OnboardingForm()

    return render(request, 'auth/onboarding.html', {'form': form})