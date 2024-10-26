from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    logo = models.ImageField(upload_to='user_logo', null=True, blank=True)