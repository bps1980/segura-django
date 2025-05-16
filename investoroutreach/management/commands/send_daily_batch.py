import os
import time
from django.core.management.base import BaseCommand
from django.utils import timezone
from investoroutreach.models import Investor, EmailLog
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Asm

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")
GROUP_ID = 28149  # Your SendGrid unsubscribe group ID

class Command(BaseCommand):
    help = "Send daily email batch to 25000 US-based investors"

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        sent_today = EmailLog.objects.filter(created_at__date=today).count()

        if sent_today >= 25000:
            self.stdout.write("📬 Daily limit of 25000 emails already reached.")
            return

        # Get US-based investors who haven’t been emailed yet
        us_batch = list(
            Investor.objects.filter(country__iexact='United States')
            .exclude(email__in=EmailLog.objects.values_list('recipient_email', flat=True))
        )[:25000 - sent_today]

        if not us_batch:
            self.stdout.write("⚠️ No eligible US investors found.")
            return

        sg = SendGridAPIClient(SENDGRID_API_KEY)
        count = 0

        for inv in us_batch:
            print(f"👉 Candidate: {inv.email} ({inv.investor_type}, {inv.country})")

            if not inv.email or "@" not in inv.email:
                print(f"❌ Skipping invalid email: {inv.email}")
                continue

            html = self.build_email_body(inv)

            message = Mail(
                from_email=FROM_EMAIL,
                to_emails=inv.email,
                subject="Strategic Investment Opportunity – Segura Mgmt",
                html_content=html
            )

            message.asm = Asm(group_id=GROUP_ID)

            try:
                response = sg.send(message)
                print(f"✅ SENT to {inv.email} - Status: {response.status_code}")
                EmailLog.objects.create(
                    company=inv.company_name,
                    recipient_email=inv.email,
                    country=inv.country,
                    success=(200 <= response.status_code < 300)
                )
                count += 1
                time.sleep(1)  # Respect API rate limits
            except Exception as e:
                print(f"❌ ERROR sending to {inv.email} - {e}")
                EmailLog.objects.create(
                    company=inv.company_name,
                    recipient_email=inv.email,
                    country=inv.country,
                    success=False
                )

        self.stdout.write(self.style.SUCCESS(f"✅ Successfully sent {count} emails."))

    def build_email_body(self, inv):
        return f"""
        <html><body>
        <p>Dear {inv.company_name or 'Investor'},</p>
        <p>I hope you're well. I'm reaching out to invite you to explore Segura Mgmt's high-impact portfolio in AI, aerospace, fintech, and blockchain.</p>
        <p>
            <a href="https://app.seguramgmt.com/click/{inv.id}" style="color:#007bff;">View Our Investment Deck</a>
        </p>
        <p>We realize this may be a duplicate message, as some recipients were unable to access our site earlier. The issue has been resolved.</p>
        <p>I’d love to personally help and answer any questions you may have.</p>
        <p>Best regards,<br>Brennen Segura<br><a href="mailto:brennen@seguramgmt.com">brennen@seguramgmt.com</a></p>
        <hr>
        <p style="font-size:12px; color:#888;">
            You are receiving this message because of your publicly listed contact.<br>
            <a href="<%asm_group_unsubscribe_raw_url%>">Unsubscribe</a>
        </p>
        </body></html>
        """
