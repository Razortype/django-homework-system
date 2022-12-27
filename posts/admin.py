from django.contrib import admin

from .models import Homework, HomeworkDetail, Post

# Register your models here.
admin.site.register(Homework)
admin.site.register(HomeworkDetail)
admin.site.register(Post)