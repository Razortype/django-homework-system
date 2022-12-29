from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login, logout

from posts.models import Post
from .models import Person
from .forms import LoginForm, UpdateUserForm, UpdatePersonForm

from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class LoginView(View):

    form_class = LoginForm

    def post(self, req, *args, **kwargs):
        form = self.form_class(data=req.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(req, username=username, password=password)

            if user is not None:
                login(req, user)

                redirect_to = req.GET.get("next")
                if redirect_to is None:
                    return HttpResponseRedirect("/homeworks")
                else:
                    return HttpResponseRedirect(redirect_to)
            else:
                return HttpResponse("You cannot login with these credentials")

        else:
            return HttpResponse("Form is not valid")

    def get(self, req, *args, **kwargs):
        form = self.form_class()
        content = {'title': 'Login', 'style_file': 'users/css/login.css', 'form': form}
        return HttpResponse(render(req, 'users/login.html', content))

class LogoutView(View):
    def get(self, req, *args, **kwargs):
        user = req.user
        if isinstance(user, AnonymousUser):
            return HttpResponse("You have to login first")
        else:
            logout(req)
            return HttpResponseRedirect("/")

## General

class Home(View):

    def get(self, req, *args, **kwargs):
        user = req.user
        content = {
            'style_file': 'partials/css/home.css',
            'js_file': 'partials/js/_header.js'
        }

        if not isinstance(user, AnonymousUser):
            content['person'] = Person.objects.get(pk=user.id)

        return HttpResponse(render(req, 'home.html', content))

# Profile

class Profile(LoginRequiredMixin, View):

    user_form = UpdateUserForm
    person_form = UpdatePersonForm

    def get(self, req, *args, **kwargs):
        user = req.user
        content = {'title': 'WEB | Profil'}
        content['posts'] = Post.objects.filter(person__user__id = user.id)

        if not isinstance(user, AnonymousUser):
            content['person'] = Person.objects.get(pk=user.id)

        return HttpResponse(render(req, 'users/profile.html', content))

    def post(self, req, *args, **kwargs):
        return HttpResponse("NOT FOUND")