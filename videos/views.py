from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin

from users.models import Person
from .models import Video

class VideoList(LoginRequiredMixin, View):

    login_url = "login"
    redirect_field_name = "next"

    def get(self, req, *args, **kwargs):

        user = req.user

        content = {
            'title': 'WEB | Videolar',
            'videos': Video.objects.all(),
            'style_file': 'videos/css/video_list.css',
        }

        if not isinstance(user, AnonymousUser):
            content['person'] = Person.objects.get(pk=user.id)

        return HttpResponse(render(req, 'videos/video_list.html', content))
