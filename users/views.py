from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login, logout

from posts.models import Post
from .models import Person, CustomUser, SignUserModel, UserToken
from .forms import LoginForm, UpdateUserForm, PersonForm, SignUserForm, TokenForm, ForgotPasswordForm, EmailForm
from .utils import generate_token, EmailThread, check_password_valid, check_account_valid, generate_forgot_token

from django.contrib import messages 
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError

from django.core.mail import EmailMessage
from django.conf import settings

def send_verification_email(user: CustomUser, req):
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

def send_forgot_email(user: CustomUser, token, req):
    person = Person.objects.get(pk=user.pk)
    current_site = get_current_site(req)
    email_subject = "Email şifre değiştirme"
    email_body = render_to_string("users/forgot_email.html", {
        'person': person,
        'domain': current_site,
        'token': token,
    })

    email = EmailMessage(
        subject = email_subject,
        body = email_body,
        from_email = settings.EMAIL_FROM_USER,
        to = [user.email]
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
            messages.error(req, "Kullanıcı adı veya Şifre hatalı")
            return HttpResponseRedirect('/login')

        if not user.is_email_valid:
            messages.warning(req, "Emailinizi aktive etmeniz gerekmektedir")
            return HttpResponseRedirect('/login')
        else:
            login(req, user)
            messages.success(req, "Başarıyla giriş yapıldı")

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
            messages.error(req, "Çıkış yapabilmek için önce giriş yapmanız gerekmektedir")
            return HttpResponseRedirect('/login')
        else:
            logout(req)
            messages.success(req, "Başarıyla çıkış yapıldı")
            return HttpResponseRedirect("/")


class Register(View):

    user_form = SignUserForm
    person_form = PersonForm

    def get(self, req, *args, **kwargs):
        content = {
            'user_form': self.user_form(),
            'person_form': self.person_form(),
            'style_file': 'users/css/register.css',
            'js_files': [
                'users/js/register.js',
                'partials/js/_navbar.js'
                ],
        }

        return HttpResponse(render(req, 'users/register.html', content))

    def post(self, req, *args, **kwargs):
        
        user_form = self.user_form(req.POST)
        person_form = self.person_form(req.POST)

        if user_form.is_valid() and person_form.is_valid():
            
            account_errors = check_account_valid(user_form.cleaned_data['username'], user_form.cleaned_data['email'], person_form.cleaned_data['github_url'])

            if account_errors:
                for error in account_errors:
                    messages.error(req, error)
                return HttpResponseRedirect('/register')

            password_errors = check_password_valid(user_form.cleaned_data['password1'],user_form.cleaned_data['password2'])

            if password_errors:
                for error in password_errors:
                    messages.error(req, error)
                return HttpResponseRedirect('/register')
            
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

            send_verification_email(user, req)

            messages.info(req, "Emailinize aktivasyon kodu gönderilmiştir")
            return HttpResponseRedirect('/login')

        else:
            messages.error(req, "Girilen bilgiler doğru belirtilmedi")
            return HttpResponseRedirect('/register')

class ActivateUser(View):

    def get(self, req, uidb64, token, *args, **kwargs):

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except Exception as e:
            print(e)
            user = None

        if user and generate_token.check_token(user, token):
            user.is_email_valid = True
            user.save()

            messages.success(req, "Emailiniz başarıyla aktive edildi")
            return HttpResponseRedirect('/login')

        messages.warning(req, "Email onaylanması sırasında bir hata gerçekleşti")
        return HttpResponseRedirect('/')

class ForgotPasswordGenerate(View):

    email_form = EmailForm

    def get(self, req, *args, **kwargs):
        
        content = {
            'form': self.email_form()
        }
        return HttpResponse(render(req, 'users/password_forgot_email.html', content))

    def post(self, req, *args, **kwargs):
        
        email_form = self.email_form(req.POST)

        if not email_form.is_valid():
            messages.error(req, "Girilen veri uygun beriltilmelidir")
            return HttpResponseRedirect('/users/password-forget')

        try:
            user = CustomUser.objects.get(email=email_form.cleaned_data['email'])
        except CustomUser.DoesNotExist:
            user = None

        if user is None:
            messages.warning(req, "Böyle bir kullanıcı bulunmamaktadır")
            messages.info(req, "Hemen kayıt olabilirsiniz")
            return HttpResponseRedirect('/register')

        try:
            token = UserToken.objects.get(user=user)
        except UserToken.DoesNotExist:
            token = None

        generated_token = generate_forgot_token()

        if token is None:
            token = UserToken(user=user, token=generated_token)
            token.save()
        else:
            token.token = generated_token

        send_forgot_email(user, token.token, req)

        messages.success(req, "Şifre değiştirme kodu emailinize gönderildi")
        return HttpResponseRedirect('/')

class ForgotPasswordToken(View):

    token_form = TokenForm

    def get(self, req, *args, **kwargs):

        content = {
            'form': self.token_form()
        }
        return HttpResponse(render(req, 'users/password_token.html', content))

    def post(self, req, *args, **kwargs):

        token_form = self.token_form(req.POST)

        if not token_form.is_valid():
            messages.error(req, "Girilen form geçerli değildir")
            return HttpResponseRedirect('/users/forgot-password/token')

        try:
            token_object = UserToken.objects.get(token=token_form.cleaned_data['token'])
        except UserToken.DoesNotExist:
            token_object = None

        if token_object is None:
            messages.warning(req, "Girilen token geçerli değildir")
            return HttpResponseRedirect('/login')
            
        if not token_object.check_token_valid():
            token_object.delete()
            messages.warning(req, "Girilen tokenin süresi tükenmiştir")
            return HttpResponseRedirect('/login')

        response = HttpResponseRedirect('/users/forgot-password/new')
        response.set_cookie('forgot_token', token_object.token)
        return response

class ForgotPassword(View):

    forgot_form = ForgotPasswordForm

    def get(self, req, *args, **kwargs):
        
        value = req.COOKIES.get('forgot_token')
        if value is None:
            messages.error(req, "Token olmadan şifre değiştiremezsiniz")
            return HttpResponseRedirect('/users/forgot-password/token')

        token = UserToken.objects.get(token=value)
        user = CustomUser.objects.get(pk=token.pk)

        content = {
            'user': user,
            'person_content': Person.objects.get(user=token.user),
            'form': self.forgot_form()
        }

        return HttpResponse(render(req, 'users/password_forgot.html', content))

    def post(self, req, *args, **kwargs):

        forgot_form = self.forgot_form(req.POST)

        value = req.COOKIES.get('forgot_token')
        if value is None:
            messages.error(req, "Token olmadan şifre değiştiremezsiniz")
            return HttpResponseRedirect('/')

        if not forgot_form.is_valid():
            messages.error(req, "Girdiğiniz değerler forma uygun olmalıdır")
            return HttpResponseRedirect('/users/forgot-password/new')

        errors = check_password_valid(forgot_form.cleaned_data['password1'], forgot_form.cleaned_data['password2'])

        if errors:
            for error in errors:
                messages.error(req, error)
            return HttpResponseRedirect('/users/forgot-password/new')

        token = UserToken.objects.get(token=value)
        user = CustomUser.objects.get(pk=token.pk)

        user.set_password(forgot_form.cleaned_data['password1'])
        user.save()
        
        token.delete()

        messages.success(req, "Şifreniz başarıyla değiştirildi")
        response = HttpResponseRedirect('/login')
        response.delete_cookie('forgot_token')
        return response

## General

class Home(View):

    def get(self, req, *args, **kwargs):
        user = req.user

        content = {
            'style_file': 'partials/css/home.css',
            'js_files': [
                'partials/js/_header.js'
            ],
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
        content = {
            'title': 'WEB | Profil',
            'posts': Post.objects.filter(person__user__id = user.id),
        }

        if not isinstance(user, AnonymousUser):
            content['person'] = Person.objects.get(pk=user.id)

        return HttpResponse(render(req, 'users/profile.html', content))