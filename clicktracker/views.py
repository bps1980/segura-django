from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from investoroutreach.models import EmailLog, Investor
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST

class Command(BaseCommand):  # <- THIS must be named exactly `Command`
    help = "Send follow-up emails to investors who haven't clicked within X days"

    def handle(self, *args, **kwargs):
        cutoff = timezone.now() - timedelta(days=5)

        logs = EmailLog.objects.filter(
            clicked=False,
            follow_up_sent=False,
            last_sent_at__lt=cutoff
        )

        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        from_email = os.getenv("FROM_EMAIL")

        for log in logs:
            try:
                investor = Investor.objects.get(email=log.recipient_email)

                html_content = f"""
                <html><body>
                <p>Dear {investor.company_name or 'Investor'},</p>
                <p>I wanted to follow up on our previous message about strategic investment opportunities.</p>
                <p>We're still actively engaging partners in AI, aerospace, blockchain, and GovTech.</p>
                <p>
                    <a href="https://app.seguramgmt.com/click/{investor.id}" style="color:#007bff;">View Our Investment Deck</a>
                </p>
                <p>Best regards,<br>Brennen Segura</p>
                </body></html>
                """

                message = Mail(
                    from_email=from_email,
                    to_emails=log.recipient_email,
                    subject="Following up: Segura Mgmt Strategic Opportunities",
                    html_content=html_content
                )

                sg.send(message)

                log.follow_up_sent = True
                log.save()
                self.stdout.write(self.style.SUCCESS(f"Follow-up sent to {log.recipient_email}"))

            except Exception as e:
                self.stderr.write(f"Failed to send follow-up to {log.recipient_email}: {str(e)}")
# clicktracker/views.py

def email_clicked(request, investor_id):
    investor = get_object_or_404(Investor, pk=investor_id)
    EmailLog.objects.filter(recipient_email=investor.email).update(clicked=True)

    send_mail(
        subject="Investor Clicked Link",
        message=f"{investor.company_name} ({investor.email}) clicked the campaign link.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=["brennen@seguramgmt.com"]
    )

    return redirect('https://app.seguramgmt.com')

@staff_member_required
def dashboard(request):
    logs = EmailLog.objects.all().order_by('-created_at')
    return render(request, 'clicktracker/dashboard.html', {'logs': logs})

@require_POST
@staff_member_required
def mark_reviewed(request, log_id):
    log = get_object_or_404(EmailLog, pk=log_id)
    log.reviewed = True
    log.save()
    return redirect('clicktracker:dashboard')