# Generated by Django 4.2.5 on 2025-04-25 03:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kyc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='kycsubmission',
            name='session_id',
            field=models.CharField(default='pending-session', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='kycsubmission',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kyc_submissions', to=settings.AUTH_USER_MODEL),
        ),
    ]
