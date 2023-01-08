from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

from users.models import Person
from .models import Category, Homework, HomeworkDetail, Post

from .forms import PostForm

from .utils import get_timestamp

from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin

## Homework Views

class HomeworkList(LoginRequiredMixin, View):

    login_url = "login"
    redirect_field_name = "next"

    def get(self, req, *args, **kwargs):
        user = req.user
        content = {
            'title': 'WEB | Ödevler',
            'categories': Category.objects.all(),
            'homeworks': Homework.objects.all(),
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
        content = {
            'title': f'WEB | Ödevler - {category}',
            'categories': Category.objects.all(),
            'homeworks': Homework.objects.filter(category__name = category).values(),
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

    def get(self, req, id, *args, **kwargs):
        user = req.user
        homework = Homework.objects.get(pk=id)

        content = {
            'title': f'WEB | Ödevler - {homework.name}',
            'homework' : homework,
            'details': HomeworkDetail.objects.filter(homework__id = homework.id),
            'posts': sorted(Post.objects.filter(homework__id = homework.id), key=lambda person: get_timestamp(person.post_at)),
            'posted': False,
            'update_form': self.post_form(),
            'style_file': 'posts/css/homework_detail.css',
            'js_files': [
                'partials/js/_navbar.js',
            ]
        }
        
        if not isinstance(user, AnonymousUser):
            content['person'] = Person.objects.get(pk=user.id)
            if content['person'] in [i.person for i in content["posts"]]:
                content['posted'] = True

        return HttpResponse(render(req, 'posts/homework_detail.html', content))

class HomeworkPostNew(View):

    post_form = PostForm

    def post(self, req, id, *args, **kwargs):

        user = req.user
        person = Person.objects.get(pk=user.pk)
        try:
            homework = Homework.objects.get(pk=id) 
        except Exception:
            homework = None

        if homework is None:
            messages.warning(req, "Uygun ödev bulunamamıştır")
            return HttpResponseRedirect('/homeworks')

        post_form = self.post_form(req.POST)
        if not post_form.is_valid():
            messages.warning(req, "Uygun veriler gönderilmedi")
            return HttpResponseRedirect(f'homeworks/id/{id}')

        if not post_form.cleaned_data['github_url'].startswith(person.github_url):
            messages.warning(req, "Gönderilen ödev size ait olamak zorundadır")
            return HttpResponseRedirect(f'homeworks/id/{id}')

        post = Post.objects.create(person=person, homework=homework, post_url=post_form.cleaned_data['github_url'])
        post.save()
        messages.success(req, "Post başarıyla atıldı")
        return HttpResponseRedirect(f'homeworks/id/{id}')

class HomeworkPostUpdate(View):
    def post(self, req, *args, **kwargs):

        pass

class HomeworkPostDelete(View):
    def post(self, req, *args, **kwargs):

        pass