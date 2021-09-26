from django.db import models
from django.db.models import Model


# Create your models here.

class CreatePasswordModel(Model):
    password = models.CharField(max_length=32, null=True, blank=False)
    created_date = models.DateField()
    retired_date = models.DateField(null=False, blank=False)
    used_for_website = models.CharField(max_length=70)
    explanation = models.TextField(max_length=200)
