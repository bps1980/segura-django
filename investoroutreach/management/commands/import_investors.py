import pandas as pd
import os
from django.core.management.base import BaseCommand
from investoroutreach.models import Investor
from django.db import IntegrityError

class Command(BaseCommand):
    help = "Import investor records from Excel (no email validation)"

    def handle(self, *args, **options):
        path = "/mnt/c/Users/segura23/Themeforest/SGMT2/segura-django/Investor_Database.xlsx"

        if not os.path.exists(path):
            self.stdout.write(self.style.ERROR(f"❌ File not found: {path}"))
            return

        # Choose correct reader based on file type
        try:
            if path.endswith(".csv"):
                df = pd.read_csv(path)
            else:
                df = pd.read_excel(path, engine="openpyxl")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Failed to read file: {e}"))
            return

        imported = 0
        skipped = 0

        for _, row in df.iterrows():
            email = row.get("contact_email") or row.get("2nd_email_100%_verified")
            if pd.isna(email) or not isinstance(email, str) or "@" not in email:
                skipped += 1
                continue

            try:
                Investor.objects.create(
                    company_name=row.get("company_name", ""),
                    email=email,
                    email_verified=row.get("contact_email_verified?", "") == "Yes",
                    second_email=row.get("2nd_email_100%_verified"),
                    phone_number=row.get("phone_number"),
                    investor_type=row.get("investor_type"),
                    country=row.get("country"),
                    location=row.get("location"),
                    employees=row.get("employees_people_database"),
                    number_of_investments=self.safe_int(row.get("number_of_investments")),
                    number_of_exits=self.safe_int(row.get("number_of_exits")),
                    domain=row.get("domain"),
                    industries=row.get("industries"),
                    key_people=row.get("key_people")
                )
                imported += 1
            except IntegrityError as e:
                self.stdout.write(self.style.WARNING(f"⚠️ Integrity error: {e}"))
                skipped += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Failed to import {email}: {e}"))
                skipped += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Imported {imported} investors."))
        self.stdout.write(self.style.WARNING(f"⚠️ Skipped {skipped} records."))

    def safe_int(self, val):
        try:
            return int(val) if pd.notna(val) else None
        except:
            return None
