from django.db import models
from users.models import Person

from django.utils import timezone
from django.utils.timezone import utc
from datetime import datetime

class Category(models.Model):
    name        = models.CharField(max_length=50)
    color       = models.CharField(max_length=6)
    description = models.TextField(max_length=1000)

    def __str__(self) -> str:
        return self.name

class Homework(models.Model):

    MIN_EXPIRE_DAY = 7

    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    description = models.TextField(max_length=1000, default=' ', null=False, blank=True)
    display = models.BooleanField(default=False)
    created_at = models.DateField(auto_now=True)
    start_at = models.DateField(default=timezone.now)
    expired_date = models.DateField()

    def check_exipred(self):
        if self.post_at:
            now = datetime.utcnow().replace(tzinfo=utc)
            timediff = now - self.expired_date
            return timediff.total_seconds()

    def __str__(self) -> str:
        return f"{self.name} (dp:{self.display})"

class HomeworkDetail(models.Model):
    LOW = 'L'
    NORMAL = 'N'
    HIGH = 'H'
    RISK_LEVELS = [
        (LOW, 'Low'),
        (NORMAL, 'Normal'),
        (HIGH, 'High'),
    ]

    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    detail_name = models.CharField(max_length=100)
    detail_description = models.TextField(max_length=1000, default=' ', null=False, blank=True)
    detail_risk = models.CharField(
        max_length=2,
        choices=RISK_LEVELS,
        default=LOW
    )

    def __str__(self) -> str:
        return f"{self.detail_name} - {self.homework.name}"

class Post(models.Model):
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    post_url = models.URLField(max_length=200)
    post_at = models.DateField(auto_now=True)

    def get_time_diff(self):
        if self.post_at:
            now = datetime.utcnow().replace(tzinfo=utc)
            timediff = now - self.time_posted
            return timediff.total_seconds()

    def __str__(self) -> str:
        return f"{self.person.name} - {self.homework.name}"