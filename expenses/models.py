from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# Create your models here.
Userm=get_user_model()

class User(User):
    pass