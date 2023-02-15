from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin

from posts.models import Category
from users.models import Person
from .models import Video

class VideoList(LoginRequiredMixin, View):

    login_url = "login"
    redirect_field_name = "next"

    def get(self, req, *args, **kwargs):

        user = req.user

        content = {
            'title': 'WEB | Videolar',
            'categories': [i for i in Category.objects.all() if i.get_video_amount() > 0],
            'videos': Video.objects.all().order_by("release_date"),
            'style_file': 'videos/css/video_list.css',
            'js_files': [
                'partials/js/_navbar.js',
                'videos/js/video_list.js'
            ]
        }

        if not isinstance(user, AnonymousUser):
            content['person'] = Person.objects.get(pk=user.id)

        return HttpResponse(render(req, 'videos/video_list.html', content))

class VideoListByType(LoginRequiredMixin, View):

    login_url = "login"
    redirect_field_name = "next"

    def get(self, req, category ,*args, **kwargs):

        user = req.user

        if not Category.objects.all().filter(name=category).exists():
            messages.error(req, f"Uygun kategori bulunamadı: {category}")
            return HttpResponseRedirect("/videos")

        content = {
            'title': 'WEB | Videolar',
            'categories': [i for i in Category.objects.all() if i.get_video_amount() > 0],
            'videos': Video.objects.filter(category__name=category).order_by("release_date"),
            'style_file': 'videos/css/video_list.css',
            'js_files': [
                'partials/js/_navbar.js',
                'videos/js/video_list.js'
            ]
        }

        if not isinstance(user, AnonymousUser):
            content['person'] = Person.objects.get(pk=user.id)

        return HttpResponse(render(req, 'videos/video_list.html', content))
