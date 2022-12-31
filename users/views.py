from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login, logout

from posts.models import Post
from .models import Person, CustomUser
from .forms import LoginForm, UpdateUserForm, PersonForm, SignUserForm
from .utils import generate_token, EmailThread

from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError

from django.core.mail import EmailMessage
from django.conf import settings

def send_action_email(user: CustomUser, req):
    person = Person.objects.get(pk=user.pk)
    current_site = get_current_site(req)
    email_subject = "Email aktivasyon linki"
    email_body = render_to_string("users/activate.html", {
        'person': person,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user),
    })

    email = EmailMessage(
        subject = email_subject,
        body = email_body,
        from_email = settings.EMAIL_FROM_USER,
        to=[user.email]
    )

    EmailThread(email).start()

# Authentication
class LoginView(View):

    form_class = LoginForm

    def post(self, req, *args, **kwargs):
        form = self.form_class(data=req.POST)

        if not form.is_valid():
            return HttpResponse("Form is not valid")

        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        user = authenticate(req, username=username, password=password)

        if user is None:
            return HttpResponse("You cannot login with these credentials")

        if not user.is_email_valid:
            return HttpResponse(render(req, 'users/activate_failed.html', {}))
        else:
            login(req, user)

        redirect_to = req.GET.get("next")
        if redirect_to is None:
            return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect(redirect_to)
            

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


class Register(View):

    user_form = SignUserForm
    person_form = PersonForm

    def get(self, req, *args, **kwargs):
        content = {
            'user_form': self.user_form(),
            'person_form': self.person_form(),
            #'style_file': ,
            #'js_file': ,
        }

        return HttpResponse(render(req, 'users/register.html', content))

    def post(self, req, *args, **kwargs):
        
        user_form = self.user_form(req.POST)
        person_form = self.person_form(req.POST)

        if user_form.is_valid() and person_form.is_valid():
            user = CustomUser.objects.create_user(
                username=user_form.cleaned_data['username'],
                email=user_form.cleaned_data['email'],
                password=user_form.cleaned_data['password1'],
            )

            person = Person(
                user=user,
                name=person_form.cleaned_data['name'].title(),
                surname=person_form.cleaned_data['surname'].title(),
                age=person_form.cleaned_data['age'],
                github_url=person_form.cleaned_data['github_url'],
            )

            person.save()

            send_action_email(user, req)

            return HttpResponseRedirect('/login')

        else:
            return HttpResponse("Credidentals were defined as wrong")

class ActivateUser(View):

    def get(self, req, uidb64, token, *args, **kwargs):

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except Exception as e:
            print(e)
            user = None

        print(user,generate_token.check_token(user, token))

        if user and generate_token.check_token(user, token):
            user.is_email_valid = True
            user.save()

            return HttpResponseRedirect('/login')

        return HttpResponseBadRequest("Email onaylanması sırasında hata oluştu")

## General

class Home(View):

    def get(self, req, *args, **kwargs):
        user = req.user

        content = {
            'style_file': 'partials/css/home.css',
            'js_file': 'partials/js/_header.js'
        }

        if not isinstance(user, AnonymousUser):
            if user.is_email_valid:
                content['person'] = Person.objects.get(pk=user.id)

        return HttpResponse(render(req, 'home.html', content))


# Profile

class Profile(LoginRequiredMixin, View):

    user_form = UpdateUserForm
    person_form = PersonForm

    def get(self, req, *args, **kwargs):
        user = req.user
        content = {'title': 'WEB | Profil'}
        content['posts'] = Post.objects.filter(person__user__id = user.id)

        if not isinstance(user, AnonymousUser):
            content['person'] = Person.objects.get(pk=user.id)

        return HttpResponse(render(req, 'users/profile.html', content))