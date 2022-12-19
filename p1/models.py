from django.db import models
from django.db import connections

class RandomForm(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    class Meta:
        db_table = 'random_form'
