from django import forms

from .models import Person, SignUserModel, ForgotPasswordModel
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Kullanıcı Adı",
        max_length=100,
        widget=forms.TextInput(attrs={'class' : 'form-control'})
        )
    password = forms.CharField(
        label="Şifre",
        widget=forms.PasswordInput(attrs={'class' : 'form-control', 'password' : forms.PasswordInput()})
        )

    def __str__(self):
        return self.username

class SignUserForm(forms.ModelForm):
    class Meta:
        model = SignUserModel
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

        widgets = {
            "password1":forms.widgets.PasswordInput(),
            "password2":forms.widgets.PasswordInput(),
        }

        labels = {
            'username': _("Kullanıcı Adı"),
            'password1': _("Şifre"),
            'password2': _("Şifre (Tekrar)")
        }

class ForgotPasswordForm(forms.ModelForm):
    class Meta:
        model = ForgotPasswordModel
        fields = [
            "password1",
            "password2",
        ]

        widgets = {
            "password1":forms.widgets.PasswordInput(),
            "password2":forms.widgets.PasswordInput(),
        }

        labels = {
            "password1": _("Yeni Şifre"),
            "password2": _("Yeni Şifre (Tekrar)"),
        }

class TokenForm(forms.Form):
    token = forms.CharField(label="Token", max_length=6)

class EmailForm(forms.Form):
    email = forms.EmailField(label="E-mail", max_length=100)

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            "name",
            "surname",
            "age",
            "github_url"
        ]

        labels = {
            'name': _("Ad"),
            'surname': _("Soyad"),
            'age': _("Yaş"),
            'github_url': _("Github Hesabı (url)")
        }