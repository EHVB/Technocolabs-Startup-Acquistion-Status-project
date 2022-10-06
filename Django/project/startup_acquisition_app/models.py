from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.

class form(models.Model):
    founded_at = models.IntegerField()
    funding_rounds = models.IntegerField()
    total_funding_usd = models.IntegerField()
    milestones = models.IntegerField()
    relationships = models.IntegerField()