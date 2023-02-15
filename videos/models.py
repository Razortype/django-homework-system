from django.db import models

from django.utils import timezone

class Video(models.Model):

    VIDEO_TYPE = [
        ('LES', 'Lesson'),
        ('EKS', 'Ekstras'),
        ('NON', 'Not Defined')
    ]

    name = models.CharField(max_length=100)
    category = models.ForeignKey('posts.Category',on_delete=models.CASCADE)
    video_type = models.CharField(
        max_length=3,
        choices=VIDEO_TYPE,
        default='NON'
    )
    video_id = models.CharField(max_length=100)
    release_date = models.DateField()

    def __str__(self) -> str:
        return f"{self.name} ({self.video_type} - {self.category.name})"
    