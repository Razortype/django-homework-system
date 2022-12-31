from django.contrib import admin

from .models import Person, CustomUser
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Person)