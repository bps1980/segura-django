from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import KYCSubmissionForm
from .models import KYCSubmission
from .utils.ocr import extract_text_from_id
from .utils.face_match import compare_faces
from .utils.sanctions import check_sanctions
from django.contrib.admin.views.decorators import staff_member_required



@login_required
def submit_kyc(request):
    existing = KYCSubmission.objects.filter(user=request.user).last()

    if request.method == 'POST':
        form = KYCSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            kyc = form.save(commit=False)
            kyc.user = request.user
            kyc.status = 'pending'
            kyc.save()

            # Run OCR + Face Match + Sanctions check
            text_data = extract_text_from_id(kyc.id_document.path)
            faces_match, match_msg = compare_faces(kyc.id_document.path, kyc.selfie.path)
            flagged, name_match = check_sanctions(kyc.full_name)

            kyc.notes = f"OCR Result: {text_data[:150]}...\nFace Match: {match_msg}\nSanctions: {'Flagged' if flagged else 'Clear'}"
            if not faces_match or flagged:
                kyc.status = 'rejected'
            else:
                kyc.status = 'approved'

            kyc.reviewed_at = timezone.now()
            kyc.save()

            return redirect('kyc_status')

    else:
        form = KYCSubmissionForm()

    return render(request, 'kyc/submit_kyc.html', {'form': form, 'existing': existing})

@login_required
def kyc_status(request):
    submission = KYCSubmission.objects.filter(user=request.user).last()
    return render(request, 'kyc/kyc_status.html', {'submission': submission})

@staff_member_required
def all_kyc_submissions(request):
    submissions = KYCSubmission.objects.select_related('user').order_by('-submitted_at')
    return render(request, 'kyc/all_kyc_submissions.html', {'submissions': submissions})