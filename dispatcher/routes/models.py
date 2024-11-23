from django.db import models

# Create your models here.
# models.py

from django.db import models


class RoundDetails(models.Model):
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    waypoints = models.CharField(max_length=100)
    total_distance = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

