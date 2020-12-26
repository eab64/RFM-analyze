from __future__ import unicode_literals

from django.db import models

class Information(models.Model):
    Name = models.CharField(max_length=55, null=True)
    Number = models.CharField(max_length=15, null=True)
    Income = models.FloatField(null=True)
    Visit_count = models.IntegerField(null=True)


class Additional(models.Model):
    Number = models.CharField(max_length=15, null=True)
    Visit_data = models.DateTimeField(null=True)
    Visit_status = models.TextField(null=True)
