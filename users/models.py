from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import datetime, timedelta
from django.utils.timezone import utc

# Create your models here.
class CustomUser(AbstractUser):
    is_email_valid = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username

class SignUserModel(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    password1 = models.CharField(max_length=20)
    password2 = models.CharField(max_length=20)

class ForgotPasswordModel(models.Model):
    password1 = models.CharField(max_length=20)
    password2 = models.CharField(max_length=20)

class Person(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    name = models.CharField(max_length=50, null=False, blank=False)
    surname = models.CharField(max_length=30, null=False, blank=False)
    age = models.SmallIntegerField()
    github_url = models.URLField(max_length=200)
    created_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name} {self.surname}"


class UserToken(models.Model):
    
    MAX_EXPIRE_DATE_MINUTE = 15
    
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True
    )
    token = models.CharField(max_length=6, null=False, blank=False)
    created_at = models.DateField(auto_now=True)

    def check_token_valid(self):
        now = datetime.utcnow().replace(tzinfo=utc)
        expired = datetime(self.created_at.year, self.created_at.month, self.created_at.day) + timedelta(minutes=self.MAX_EXPIRE_DATE_MINUTE)
        return now.now() < expired.now()