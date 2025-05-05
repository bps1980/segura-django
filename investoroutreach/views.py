# views.py (inside investoroutreach/)
import os
import time
import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
from django.contrib.admin.views.decorators import staff_member_required
from .models import EmailLog
from .models import Investor
from django.contrib import messages

# Load environment variables
load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")
COMPANY_ADDRESS = os.getenv("COMPANY_ADDRESS")
UNSUBSCRIBE_LINK = os.getenv("UNSUBSCRIBE_LINK")

@staff_member_required
def upload_excel(request):
    if request.method == "POST" and request.FILES.get('excel_file'):
        file = request.FILES['excel_file']
        df = pd.read_excel(file)

        # Optional: clear old records first
        # Investor.objects.all().delete()

        imported = 0
        for _, row in df.iterrows():
            email = row.get('contact_email') or row.get('2nd_email_100%_verified')
            if pd.isna(email):
                continue

            Investor.objects.create(
                company_name=row.get('company_name', ''),
                email=email,
                email_verified=row.get('contact_email_verified?', '') == 'Yes',
                second_email=row.get('2nd_email_100%_verified'),
                phone_number=row.get('phone_number'),
                investor_type=row.get('investor_type'),
                country=row.get('country'),
                location=row.get('location'),
                employees=row.get('employees_people_database'),
                number_of_investments=row.get('number_of_investments'),
                number_of_exits=row.get('number_of_exits'),
                domain=row.get('domain'),
                industries=row.get('industries'),
                key_people=row.get('key_people')
            )
            imported += 1

        messages.success(request, f"Successfully imported {imported} investor records.")
        return redirect('investoroutreach:upload_excel')

    return render(request, 'investoroutreach/upload_excel.html')

@staff_member_required
def send_emails(request):
    data = request.session.get('investor_data')
    if not data:
        return HttpResponse("No data to send emails.")

    df = pd.DataFrame.from_dict(data)
    sent_count = 0

    sg = SendGridAPIClient(SENDGRID_API_KEY)
    for _, row in df.iterrows():
        to_email = row.get("contact_email") or row.get("2nd_email_100%_verified")
        if not to_email or "@" not in to_email:
            continue

        html_content = build_email_body(
            row.get("company_name", ""),
            row.get("investor_type", ""),
            row.get("location", ""),
            investor_id=row.get("id")  # ensure this ID is from the database or set manually
        )

        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=to_email,
            subject="Strategic Investment Opportunity – Segura Mgmt",
            html_content=html_content
        )

        try:
            response = sg.send(message)
            sent_count += 1
            EmailLog.objects.create(
                company=row.get("company_name", ""),
                recipient_email=to_email,
                country=row.get("country", ""),
                success=(200 <= response.status_code < 300)
            )
            time.sleep(1)
        except Exception as e:
            EmailLog.objects.create(
                company=row.get("company_name", ""),
                recipient_email=to_email,
                country=row.get("country", ""),
                success=False
            )

    return HttpResponse(f"Successfully sent {sent_count} emails.")

def build_email_body(company_name, investor_type, location, investor_id):
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <p>Dear {company_name or 'Investor'},</p>

        <p>I hope this message finds you well. I’m reaching out on behalf of <strong>Segura Mgmt Services</strong>, where we’re building a high-impact portfolio across several transformative sectors.</p>

        <p>Our current pipeline includes:</p>

        <ul>
            <li><strong>Aerospace & Drone Technology:</strong> Development of a manned drone (MDAV) for commercial and defense sectors</li>
            <li><strong>Blockchain & Fintech:</strong> Tokenized insurance, decentralized exchanges, and secure transaction platforms</li>
            <li><strong>Artificial Intelligence:</strong> Real-time automation, predictive modeling, and machine learning integration</li>
            <li><strong>Insurance Claims Automation:</strong> AI-powered platform integrated with <strong>Xactimate ESX</strong> to streamline residential and commercial claim workflows</li>
            <li><strong>GovTech & Federal Projects:</strong> Active proposals and engagements through SBIR/STTR, including geospatial data modernization and smart infrastructure</li>
        </ul>

        <p>
            <a href="https://yourdomain.com/click/{investor_id}" style="color: #007bff;">Click here to view our investment deck</a>
        </p>

        <p>We are selectively inviting investment partners aligned with innovation, scalability, and government or enterprise-grade tech. Given your activity in {location or 'key markets'} as a {investor_type or 'strategic investor'}, we believe there’s a strong opportunity to collaborate.</p>

        <p>Best regards,<br>
        <strong>Brennen Segura</strong><br>
        Founder, Segura Mgmt Services LLC<br>
        <a href="mailto:brennen@seguramgmt.com">brennen@seguramgmt.com</a> | (337) 658-0254</p>

        <hr>
        <p style="font-size:12px; color:#888;">
            You are receiving this message due to your publicly available investment contact listing or prior opt-in.<br>
            <a href="{UNSUBSCRIBE_LINK}" style="color:#888;">Unsubscribe</a><br>
            {COMPANY_ADDRESS}
        </p>
    </body>
    </html>
    """

    
@staff_member_required
def load_from_disk(request):
    df = pd.read_excel('/mnt/c/Users/segura23/Themeforest/SGMT/Starter-Kit/Starter-Kit/Investor_Database.xlsx')
    imported = 0

    for _, row in df.iterrows():
        email = row.get('contact_email') or row.get('2nd_email_100%_verified')
        if pd.isna(email):
            continue

        Investor.objects.create(
            company_name=row.get('company_name', ''),
            email=email,
            email_verified=row.get('contact_email_verified?', '') == 'Yes',
            second_email=row.get('2nd_email_100%_verified'),
            phone_number=row.get('phone_number'),
            investor_type=row.get('investor_type'),
            country=row.get('country'),
            location=row.get('location'),
            employees=row.get('employees_people_database'),
            number_of_investments=safe_int(row.get('number_of_investments')),
            number_of_exits=safe_int(row.get('number_of_exits')),
            domain=row.get('domain'),
            industries=row.get('industries'),
            key_people=row.get('key_people')
        )

        imported += 1

    return HttpResponse(f"Imported {imported} investors from disk.")

def safe_int(val):
    return int(val) if pd.notna(val) else None