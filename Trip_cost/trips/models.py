from django.db import models
from datetime import datetime
from django_mysql.models import ListCharField

# Create your models here.
class Trip(models.Model):
    trip_name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    date = models.DateTimeField(default=datetime.now)
    members = ListCharField(base_field=models.CharField(max_length=20), size=10, max_length=(10 * 21))

    class Meta:
        ordering = ['trip_name']

    def __str__(self):
        return self.trip_name

class Transaction(models.Model):
    trip_name = models.ForeignKey(Trip, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)
    amt_from = models.CharField(max_length=30)
    amount_to = ListCharField(base_field=models.CharField(max_length=5), size=10, max_length=(10 * 6))
    amount = models.IntegerField()
