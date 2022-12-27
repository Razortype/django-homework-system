from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Person(models.Model):
    user = models.OneToOneField(
        User,
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