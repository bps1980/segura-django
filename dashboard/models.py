# certificates/models.py
from django.db import models

class Certificate(models.Model):
    investor_name = models.CharField(max_length=255)
    certificate_id = models.CharField(max_length=50)
    date_issued = models.DateField()
    signature = models.ImageField(upload_to='signatures/')
    pdf_file = models.FileField(upload_to='certificates/', blank=True)