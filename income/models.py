from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

class Income(models.Model):
    owner = models.ForeignKey(to=User,on_delete=models.CASCADE,default=None)
    description=models.TextField(max_length=255)
    source=models.CharField(max_length=255)
    date=models.DateField(default=datetime.datetime.now)
    amount=models.CharField(max_length=25)

    def __str__(self):
        return self.owner.username+" "+self.source+" "+self.amount

class Source(models.Model):
    name=models.CharField(max_length=255)

    def __str__(self):
        return self.name