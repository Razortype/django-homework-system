from django.contrib import admin

from .models import Person, CustomUser, UserVerificationToken, UserToken
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Person)
admin.site.register(UserVerificationToken)
admin.site.register(UserToken)