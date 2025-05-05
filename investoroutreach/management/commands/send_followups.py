from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from investoroutreach.models import EmailLog, Investor
import os

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")

class Command(BaseCommand):
    help = "Send follow-up emails to investors who haven't clicked within X days"

    def handle(self, *args, **kwargs):
        cutoff = timezone.now() - timedelta(days=5)

        logs = EmailLog.objects.filter(
            clicked=False,
            follow_up_sent=False,
            last_sent_at__lt=cutoff
        )

        sg = SendGridAPIClient(SENDGRID_API_KEY)

        for log in logs:
            try:
                investor = Investor.objects.get(email=log.recipient_email)

                html_content = f"""
                <html><body>
                <p>Dear {investor.company_name or 'Investor'},</p>
                <p>I wanted to follow up on our previous message about strategic investment opportunities.</p>
                <p>We're still actively engaging partners in AI, aerospace, blockchain, and GovTech.</p>
                <p>
                    <a href="https://yourdomain.com/click/{investor.id}" style="color:#007bff;">View Our Investment Deck</a>
                </p>
                <p>Best regards,<br>Brennen Segura</p>
                </body></html>
                """

                message = Mail(
                    from_email=FROM_EMAIL,
                    to_emails=log.recipient_email,
                    subject="Following up: Segura Mgmt Strategic Opportunities",
                    html_content=html_content
                )

                response = sg.send(message)

                log.follow_up_sent = True
                log.save()
                self.stdout.write(self.style.SUCCESS(f"Follow-up sent to {log.recipient_email}"))

            except Exception as e:
                self.stderr.write(f"Failed to send follow-up to {log.recipient_email}: {str(e)}")
