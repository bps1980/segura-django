from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse  # ✅ Needed for returning the PDF
from .forms import CertificateForm
from PIL import Image, ImageDraw, ImageFont
import io
import os
from django.conf import settings
from kyc.models import KYCSubmission
from investments.models import Favorite, Project
from utils.decorators import group_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from utils.decorators import twofa_required
from django.shortcuts import get_object_or_404
from dashboard.models import Investment  # 🔁 import your Investment model
from django.utils import timezone       # 🕒 import timezone for datetime
from dashboard.models import Notification
from django.contrib.auth import get_user_model


def index(request):
    projects = Project.objects.all()
    return render(request, 'dashboard/index.html', {'projects': projects})

def dashboard(request):
    projects = Project.objects.all()
    return render(request, 'dashboard/index.html', {'projects': projects})

def dashboard_view(request):
    # Get latest KYC submission
    user_kyc = KYCSubmission.objects.filter(user=request.user).order_by('-submitted_at').first()

    # Redirect if no KYC or not approved
    if not user_kyc or user_kyc.status != 'approved':
        return redirect('submit_kyc')

    # Include KYC status in context
    kyc_status = user_kyc.status if user_kyc else None

    # Include your other context (like projects)
    projects = Project.objects.all()

    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()

    return render(request, 'dashboard/index.html', {
        'projects': projects,
        'kyc_status': kyc_status,
        'unread_count': unread_count,  # 👈 add this
    })

@login_required
def interested_projects_view(request):
    favorites = Favorite.objects.filter(user=request.user)
    projects = [fav.project for fav in favorites]
    return render(request, 'dashboard/interested.html', {
        'projects': projects
    })
    


@csrf_exempt
@login_required
def toggle_favorite(request, project_id):
    if request.method == 'POST':
        project = Project.objects.get(pk=project_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, project=project)

        if not created:
            favorite.delete()
            return JsonResponse({'status': 'removed'})
        else:
            return JsonResponse({'status': 'added'})


# Static dashboard pages
def account_settings(request): return render(request, 'dashboard/settings.html')
def invested_projects(request): return render(request, 'dashboard/invested.html')
def interested_projects(request): return render(request, 'dashboard/interested.html')
def investment_payments(request): return render(request, 'dashboard/payments.html')
def investment_agreements(request): return render(request, 'dashboard/agreements.html')
def investment_receipts(request): return render(request, 'dashboard/receipts.html')
def pitch_decks(request): return render(request, 'dashboard/pitch_decks.html')
def investor_certificates(request): return render(request, 'dashboard/certificates.html')
def regulatory_docs(request): return render(request, 'dashboard/regulations.html')
def kyc_list(request): return render(request, 'kyc/list.html')


# ✅ PDF certificate generator view
def generate_certificate_view(request):
    if request.method == 'POST':
        form = CertificateForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['investor_name']
            cert_id = form.cleaned_data['certificate_id']
            date = form.cleaned_data['date_issued']
            signature = form.cleaned_data.get('signature')

            # Load certificate background
            template_path = os.path.join(settings.BASE_DIR, 'static', 'certificates', 'sample_certificate.png')
            if not os.path.exists(template_path):
                return HttpResponse("Certificate template not found.", status=404)

            image = Image.open(template_path)
            draw = ImageDraw.Draw(image)

            # Load font
            font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'arial.ttf')
            if not os.path.exists(font_path):
                return HttpResponse("Font file not found.", status=404)

            font_large = ImageFont.truetype(font_path, 48)
            font_small = ImageFont.truetype(font_path, 30)

            # Draw text
            draw.text((480, 400), name, font=font_large, fill='black')
            draw.text((480, 500), cert_id, font=font_small, fill='black')
            draw.text((480, 600), date.strftime("%B %d, %Y"), font=font_small, fill='black')

            # Add signature if uploaded
            if signature:
                sig_image = Image.open(signature)
                sig_image = sig_image.resize((200, 100))
                image.paste(sig_image, (480, 700))

            # Output as PDF
            output = io.BytesIO()
            image.save(output, format='PDF')
            output.seek(0)

            return HttpResponse(output, content_type='application/pdf')

    else:
        form = CertificateForm()

    return render(request, 'dashboard/generate_certificate_form.html', {'form': form})

@group_required('Employee')
def employee_view(request):
    return render(request, 'dashboard/employee_home.html')

@group_required('Admin')
def admin_view(request):
    submissions = KYCSubmission.objects.all().order_by('-submitted_at')
    return render(request, 'kyc/all_kyc_submissions.html', {'submissions': submissions})

@login_required
@twofa_required
def stripe_checkout(request, investment_id):
    # Only allow if user has passed 2FA
    ...

@login_required
@twofa_required
def test_protected_view(request):
    return HttpResponse("✅ You passed 2FA and can access this protected view.")

@login_required
def investment_agreement_view(request, investment_id):
    investment = get_object_or_404(Investment, id=investment_id, investor__user=request.user)

    if request.method == 'POST':
        investment.agreement_signed = True
        investment.agreement_signed_at = timezone.now()
        investment.save()
        return redirect('dashboard')  # or next step (like payment)

    return render(request, 'dashboard/agreements.html', {
        'investment': investment,
        'user': request.user,
        'agreement': {
            'date': timezone.now().date()
        }
    })
    
@login_required
def dashboard_home(request):
    try:
        kyc = KYCSubmission.objects.filter(user=request.user).latest('submitted_at')
        if kyc.status != 'approved':
            return redirect('kyc_status')
    except KYCSubmission.DoesNotExist:
        return redirect('kyc_status')

    return render(request, 'dashboard/index.html')

@login_required
def profile_view(request):
    return render(request, 'dashboard/profile.html')

@login_required
def settings_view(request):
    return render(request, 'dashboard/settings.html')

@login_required
def help_view(request):
    # Example notification added when user visits Help
    Notification.objects.create(
        user=request.user,
        message="Visited the Help Center.",
        link="/dashboard/help/"
    )
    return render(request, 'dashboard/help.html')

@login_required
def investment_success(request):
    Notification.objects.create(
        user=request.user,
        message="You successfully invested $5,000 in SeguraSafeSwap.",
        link="/dashboard/invested/"
    )
    return redirect('invested_projects')

User = get_user_model()

def send_maintenance_notification():
    User = get_user_model()
    for user in User.objects.all():
        Notification.objects.create(
            user=user,
            message="Platform maintenance scheduled May 10, 2:00 AM UTC.",
            link="/dashboard/"
        )
        
@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:10]
    return render(request, 'dashboard/notifications.html', {'notifications': notifications})
