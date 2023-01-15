from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

from users.models import Person
from .models import Category, Homework, HomeworkDetail, Post

from .forms import PostForm

from .utils import get_timestamp, seperate_homeworks

from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin

## Homework Views

class HomeworkList(LoginRequiredMixin, View):

    login_url = "login"
    redirect_field_name = "next"

    def get(self, req, *args, **kwargs):
        user = req.user

        enabled_homeworks, disabled_homeworks = seperate_homeworks(Homework.objects.all())

        content = {
            'title': 'WEB | Ödevler',
            'categories': Category.objects.all(),
            'homeworks': enabled_homeworks + disabled_homeworks,
            'style_file': 'posts/css/homework_list.css',
            'js_files': [
                'partials/js/_navbar.js'
            ]
        }

        if not isinstance(user, AnonymousUser):
            content['person'] = Person.objects.get(pk=user.id)

        return HttpResponse(render(req, 'posts/homework_list.html', content))

class HomeworkListByType(LoginRequiredMixin, View):

    login_url = "login"
    redirect_field_name = "next"

    def get(self, req, category, *args, **kwargs):
        user = req.user

        enabled_homeworks, disabled_homeworks = seperate_homeworks(Homework.objects.filter(category__name = category))

        content = {
            'title': f'WEB | Ödevler - {category}',
            'categories': Category.objects.all(),
            'homeworks': enabled_homeworks + disabled_homeworks,
            'style_file': 'posts/css/homework_list.css',
            'js_files': [
                'partials/js/_navbar.js',
            ]
        }

        if not isinstance(user, AnonymousUser):
            content['person'] = Person.objects.get(pk=user.id)

        return HttpResponse(render(req, 'posts/homework_list.html', content))

class HomeworkDetailById(LoginRequiredMixin, View):

    login_url = "login"
    redirect_field_name = "next"

    post_form = PostForm

    def get(self, req, _id, *args, **kwargs):
        user = req.user
        homework = Homework.objects.get(pk=_id)

        content = {
            'title': f'WEB | Ödevler - {homework.name}',
            'homework' : homework,
            'details': HomeworkDetail.objects.filter(homework__id = homework.id),
            'posts': sorted(Post.objects.filter(homework__id = homework.id), key=lambda person: get_timestamp(person.post_at)),
            'form': self.post_form(),
            'personpost': None,
            'style_file': 'posts/css/homework_detail.css',
            'js_files': [
                'partials/js/_navbar.js',
            ]
        }
        
        if not isinstance(user, AnonymousUser):
            content['person'] = Person.objects.get(pk=user.id)
            if content['person'] in [i.person for i in content["posts"]]:
                content['personpost'] = Post.objects.get(person = content['person'])

        return HttpResponse(render(req, 'posts/homework_detail.html', content))

    def post(self, req, *args, **kwargs):
        return HttpResponseRedirect('/homeworks')

class HomeworkPostNew(LoginRequiredMixin, View):

    post_form = PostForm
    login_url = "login"
    redirect_field_name = "next"

    def post(self, req, _id, *args, **kwargs):

        user = req.user
        person = Person.objects.get(pk=user.pk)

        try:
            homework = Homework.objects.get(pk=_id) 
        except Exception:
            homework = None

        if homework is None:
            messages.warning(req, "Uygun ödev bulunamamıştır")
            return HttpResponseRedirect('/homeworks')

        homework_page_url = f'/homeworks/id/{homework.pk}/detail'

        post_form = self.post_form(req.POST)
        if not post_form.is_valid():
            messages.warning(req, "Uygun veriler gönderilmedi")
            return HttpResponseRedirect(homework_page_url)

        if not post_form.cleaned_data['github_url'].startswith(person.github_url):
            messages.warning(req, "Gönderilen ödev size ait olamak zorundadır")
            return HttpResponseRedirect(homework_page_url)

        post = Post.objects.create(person=person, homework=homework, post_url=post_form.cleaned_data['github_url'])
        post.save()
        messages.success(req, "Post başarıyla atıldı")
        return HttpResponseRedirect(homework_page_url)

class HomeworkPostUpdate(LoginRequiredMixin, View):

    update_post = PostForm
    login_url = "login"
    redirect_field_name = "next"

    def post(self, req, homework_id, post_id, *args, **kwargs):

        update_form = self.update_post(req.POST)
        return_url = f'/homeworks/id/{homework_id}/detail'

        try:
            post = Post.objects.get(pk=post_id)
        except Exception:
            post = None

        if post is None:
            messages.warning(req, "Aranılan post bulunamadı")
            return HttpResponseRedirect(return_url)

        if post.person != req.user.person:
            messages.warning(req, "Postu atan kişi siz olmak zorundasınız")
            return HttpResponseRedirect(return_url)

        if not update_form.is_valid():
            messages.warning(req, "Girilen veriler geçerli değildir")
            return HttpResponseRedirect(return_url)

        if not update_form.cleaned_data['github_url'].startswith(req.user.person.github_url):
            messages.warning(req, "Gönderilen ödev size ait olamak zorundadır")
            return HttpResponseRedirect(return_url)

        post.post_url = update_form.cleaned_data['github_url']
        post.save()
        messages.success(req, 'Post başarıyla değiştirildi')
        return HttpResponseRedirect(return_url)

class HomeworkPostDelete(LoginRequiredMixin, View):

    login_url = "login"
    redirect_field_name = "next"

    def get(self, req, homework_id, post_id, *args, **kwargs):

        return_url = f'/homeworks/id/{homework_id}/detail'
        try:
            post = Post.objects.get(pk=post_id)
        except Exception:
            post = None

        if post is None:
            messages.warning(req, "Aranılan post bulunamadı")
            return HttpResponseRedirect(return_url)

        if post.person != req.user.person:
            messages.warning(req, "Postu atan kişi siz olmak zorundasınız")
            return HttpResponseRedirect(return_url)

        post.delete()
        messages.success(req, "Post başarıyla silindi")
        return HttpResponseRedirect(return_url)