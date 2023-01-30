from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import datetime, timedelta
from django.utils import timezone

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
    photo = models.ImageField(upload_to="users/media/photos", blank=True)
    created_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name} {self.surname} ({self.user.username})"

class UserVerificationToken(models.Model):

    MAX_EXPIRE_DATE_MINUTE = 5

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True
    )
    token = models.CharField(max_length=39, null=False, blank=False)
    created_at = models.DateTimeField(auto_now=True)

    def check_token_valid(self):
        now = timezone.now()
        expired = self.created_at + timedelta(minutes=self.MAX_EXPIRE_DATE_MINUTE)
        return now < expired

class UserToken(models.Model):
    
    MAX_EXPIRE_DATE_MINUTE = 2
    
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True
    )
    token = models.CharField(max_length=6, null=False, blank=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user.username} ({self.token})"

    def check_token_valid(self):
        now = timezone.now()
        expired = self.created_at + timedelta(minutes=self.MAX_EXPIRE_DATE_MINUTE)
        return now < expired