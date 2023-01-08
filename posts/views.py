from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

from users.models import Person
from .models import Category, Homework, HomeworkDetail, Post

from .forms import PostForm

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
            'posts': Post.objects.filter(homework__id = homework.id),
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

    def post(self, req, *args, **kwargs):

        user = req.user
        form = self.post_form(req.POST)

        if not isinstance(user, AnonymousUser):

            if form.is_valid():
                if form.cleaned_data['user'].id == user.id:
                    # form.save()
                    messages.info("Post başarıyla atıldı")
            else:
                messages.error("Post gönderilemedi")
            
            return HttpResponseRedirect(req.path_info)
        
        else:
            messages.warning("Post atmak için önce giriş yapmalısın")
            return HttpResponseRedirect('/login')

        '''
        messages.info("Post send successfully")
        return HttpResponseRedirect(RETURN_CURRENT_PAGE)
        '''