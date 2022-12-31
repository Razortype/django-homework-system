from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from users.models import Person, CustomUser
from .models import Homework, HomeworkDetail, Post

from .forms import NewPostForm

from django.contrib.auth.mixins import LoginRequiredMixin

## Homework Views

class HomeworkList(LoginRequiredMixin, View):

    login_url = "login"
    redirect_field_name = "next"

    def get(self, req, *args, **kwargs):
        user = req.user
        content = {'title': 'WEB | Ödevler'}
        content['homeworks'] = Homework.objects.all()
        content['style_file'] = 'posts/css/homework_list.css'

        if not isinstance(user, CustomUser):
            content['person'] = Person.objects.get(pk=user.id)

        return HttpResponse(render(req, 'posts/homework_list.html', content))

class HomeworkListByType(LoginRequiredMixin, View):

    login_url = "login"
    redirect_field_name = "next"

    def get(self, req, type_name, *args, **kwargs):
        user = req.user
        content = {'title': f'WEB | Ödevler - {type_name}'}
        content['homeworks'] = Homework.objects.filter(content=type_name).values()
        content['style_file'] = 'posts/css/homework_list.css'

        if not isinstance(user, CustomUser):
            content['person'] = Person.objects.get(pk=user.id)

        return HttpResponse(render(req, 'posts/homework_list.html', content))

class HomeworkDetailById(LoginRequiredMixin, View):

    login_url = "login"
    redirect_field_name = "next"

    new_post_form = NewPostForm

    content = {}

    def get(self, req, id, *args, **kwargs):
        user = req.user
        homework = Homework.objects.get(pk=id)

        content = {
            'title': f'WEB | Ödevler - {homework.name}',
            'homework' : homework,
            'details': HomeworkDetail.objects.filter(homework__id = homework.id),
            'posts': Post.objects.filter(homework__id = homework.id),
            'posted': False,
            'update_form': self.new_post_form(),
            'style_file': 'posts/css/homework_detail.css',
        }
        
        if not isinstance(user, CustomUser):
            content['person'] = Person.objects.get(pk=user.id)
            if content['person'] in [i.person for i in content["posts"]]:
                content['posted'] = True

        return HttpResponse(render(req, 'posts/homework_detail.html', content))

    def post(self, req, *args, **kwargs):

        return HttpResponse("NOT VALIDATED HTML PAGE")
