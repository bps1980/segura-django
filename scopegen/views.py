# scopegen/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ScopeOfWorkForm
from .models import ScopeOfWork
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.mail import EmailMessage
from django.conf import settings
from io import BytesIO
import openai
from django.views.decorators.http import require_POST

client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

def scope_pdf_view(request, pk):
    scope = get_object_or_404(ScopeOfWork, pk=pk)
    template = get_template('scopegen/scope_pdf.html')
    html = template.render({'scope': scope})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="scope_{pk}.pdf"'

    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf)
    if pisa_status.err:
        return HttpResponse("PDF generation failed", status=500)

    pdf.seek(0)
    response.write(pdf.read())
    return response

def scope_result_view(request, pk):
    scope = get_object_or_404(ScopeOfWork, pk=pk)
    return render(request, 'scopegen/scope_result.html', {'scope': scope})


def generate_scope(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=700,
        temperature=0.5,
    )
    return response.choices[0].message.content


def send_scope_pdf_email(user_email, scope):
    template = get_template('scopegen/scope_pdf.html')
    html = template.render({'scope': scope})
    pdf = BytesIO()
    pisa.CreatePDF(html, dest=pdf)
    pdf.seek(0)

    email = EmailMessage(
        subject="Your Scope of Work PDF",
        body="Attached is the generated Scope of Work.",
        from_email="noreply@yourdomain.com",
        to=[user_email],
    )
    email.attach(f"scope_{scope.pk}.pdf", pdf.read(), 'application/pdf')
    email.send()


def scope_form_view(request):
    if request.method == 'POST':
        form = ScopeOfWorkForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            prompt = f"""Create a professional Scope of Work for a {instance.get_category_display()} project:
- Project Type: {instance.project_type}
- Industry: {instance.industry}
- Goals: {instance.goals}
- Tools: {instance.tools}
- Timeline: {instance.timeline}
"""
            instance.generated_scope = generate_scope(prompt)
            if request.user.is_authenticated:
                instance.user = request.user
            instance.save()

            if request.user.is_authenticated and request.user.email:
                send_scope_pdf_email(request.user.email, instance)

            return redirect('scopegen:scope_result', pk=instance.pk)
    else:
        form = ScopeOfWorkForm()
    return render(request, 'scopegen/scope_form.html', {'form': form})


@login_required
def scope_history_view(request):
    scopes = ScopeOfWork.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'scopegen/scope_history.html', {'scopes': scopes})


def scope_public_view(request, uuid):
    scope = get_object_or_404(ScopeOfWork, share_uuid=uuid, is_shared=True)
    return render(request, 'scopegen/scope_public.html', {'scope': scope})


def duplicate_scope(request, pk):
    original = get_object_or_404(ScopeOfWork, pk=pk, user=request.user)
    if request.method == 'POST':
        new_instance = ScopeOfWork.objects.create(
            user=request.user,
            project_type=original.project_type,
            industry=original.industry,
            goals=original.goals,
            tools=original.tools,
            timeline=original.timeline,
            category=original.category,
            generated_scope=original.generated_scope,
        )
        return redirect('scopegen:scope_result', pk=new_instance.pk)
    return render(request, 'scopegen/duplicate_confirm.html', {'original': original})

@require_POST
@login_required
def toggle_pitch_ready(request, pk):
    scope = get_object_or_404(ScopeOfWork, pk=pk, user=request.user)
    scope.is_pitch_ready = not scope.is_pitch_ready
    scope.save()
    return redirect('scopegen:scope_result', pk=pk)
