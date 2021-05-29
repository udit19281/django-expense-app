from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
# Create your models here.


class User(AbstractUser):
    pass

class Expenses(models.Model):
    owner = models.ForeignKey(to=User,on_delete=models.CASCADE,default=None)
    description=models.TextField(max_length=255)
    category=models.CharField(max_length=255)
    date=models.DateField(default=datetime.datetime.now)
    amount=models.CharField(max_length=25)

class Userpref(models.Model):
    username=models.CharField(max_length=50)
    currency=models.CharField(max_length=50)

    def __str__(self):
        return self.username+" prefers "+self.currency

class Category(models.Model):
    name=models.CharField(max_length=255)

    def __str__(self):
        return self.name


