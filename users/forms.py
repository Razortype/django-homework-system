from django import forms

from .models import Person
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class' : 'form-control'})
        )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class' : 'form-control', 'password' : forms.PasswordInput()})
        )

    def __str__(self):
        return self.username

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class UpdatePersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'