# investoroutreach/management/commands/resend_broken_clicks.py
from django.core.management.base import BaseCommand
from investoroutreach.models import EmailLog, Investor
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os, time

class Command(BaseCommand):
    help = "Resend emails to investors who clicked broken links"

    def handle(self, *args, **kwargs):
        logs = EmailLog.objects.filter(clicked=True, success=False)

        if not logs.exists():
            self.stdout.write("No broken-click emails found.")
            return

        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        FROM_EMAIL = os.getenv("FROM_EMAIL")
        GROUP_ID = 28149

        for log in logs:
            try:
                investor = Investor.objects.get(email=log.recipient_email)
                html = f"""
                <html><body>
                <p>Dear {investor.company_name or 'Investor'},</p>
                <p>We noticed you clicked our last message but were unable to reach our site.</p>
                <p>
                    <a href="https://app.seguramgmt.com/clicktracker/click/{investor.id}" style="color:#007bff;">Click here to view our investment deck</a>
                </p>
                <p>We’re excited to hear from you.</p>
                <p>Best,<br>Brennen Segura</p>
                </body></html>
                """

                message = Mail(
                    from_email=FROM_EMAIL,
                    to_emails=log.recipient_email,
                    subject="Correction: View Our Investment Deck – Segura Mgmt",
                    html_content=html
                )
                message.asm = { "group_id": GROUP_ID }

                sg.send(message)
                self.stdout.write(f"✅ Resent to {log.recipient_email}")
                time.sleep(1)

            except Exception as e:
                self.stderr.write(f"❌ Failed to resend to {log.recipient_email}: {e}")
