from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from django.contrib import messages 
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin

from .utils import get_commands, run_sh

def handler403(request, exception):

    content = {
        'title': 'Web | 403',
        'style_file': 'partials/css/_403.css',
        'js_files': [
            'partials/js/_403.js'
        ]
    }

    return HttpResponse(render(request, 'partials/_403.html', content))

def handler404(request, exception):

    content = {
        'title': 'Web | 404',
        'style_file': 'partials/css/_404.css',
        'js_files': [
            'partials/js/_404.js'
        ]
    }
    return HttpResponse(render(request, 'partials/_404.html', content))

def handler500(request, *args, **argv):
    content = {
        'title': 'Web | 500',
        'style_file': 'partials/css/_500.html',
        'js_files': [
            'partials/js/_500.js'
        ]
    }
    return HttpResponse(render(request, 'partials/_500.html', content))

######################### Handler Test Views ###########################

def handler403Test(request):
    content = {
        'title': 'Web | 403',
        'style_file': 'partials/css/_403.css',
        'js_files': [
            'partials/js/_403.js'
        ]
    }

    return HttpResponse(render(request, 'partials/_403.html', content))

def handler404Test(request):
    content = {
        'title': 'Web | 404',
        'style_file': 'partials/css/_404.css',
        'js_files': [
            'partials/js/_404.js'
        ]
    }
    return HttpResponse(render(request, 'partials/_404.html', content))

def handler500Test(request):
    content = {
        'title': 'Web | 500',
        'style_file': 'partials/css/_500.html',
        'js_files': [
            'partials/js/_500.js'
        ]
    }
    return HttpResponse(render(request, 'partials/_500.html', content))

# Server Controller View Created TEST
class ServerController(LoginRequiredMixin, View):

    def get(self, req, *args, **kwargs):

        if not req.user.is_superuser:
            messages.warning(req, "Bu sayfaya giriş izininiz bulunmamaktadır")
            return HttpResponseRedirect('/')

        content = {
            'commands': get_commands().keys()
        }
        return HttpResponse(render(req, 'commands.html', content))

    def post(self, req, *args, **kwargs):
        
        if not req.user.is_superuser and not isinstance(req.user, AnonymousUser):
            messages.warning(req, "Bu sayfada işlem izininiz bulunmamaktadır")
            return HttpResponseRedirect('/')
        
        commands = get_commands()
        command_name = None

        for name in commands.keys():
            if name in req.POST:
                command_name = name

        if command_name is None:
            messages.error(req, "Komut bulunamadı")
            return HttpResponseRedirect('/server-commands')

        sh_file = commands[command_name]
        run_sh(sh_file)

        messages.success(req, "Komut başarıyla aktive edildi.")
        return HttpResponseRedirect('/server-commands')
        
# Application Handler Views

class ApplicationHandler:

    class PostsURLHandler(LoginRequiredMixin, View):

        login_url = "login"
        redirect_field_name = "next"
        
        def get(self, req, *args, **kwargs):
            messages.error(req, "Ödevler sayfası geçici süreyle kapatılmıştır. En kısa zamanda düzeltilecektir.")
            return HttpResponseRedirect('/')

        def post(self, req, *args, **kwargs):
            return self.get(req)

    class VideosURLHandler(LoginRequiredMixin, View):

        login_url = "login"
        redirect_field_name = "next"

        def get(self, req, *args, **kwargs):
            messages.error(req, "Videolar sayfası geçici süreyle kapatılmıştır. En kısa zamanda düzeltilecektir.")
            return HttpResponseRedirect('/')

        def post(self, req, *args, **kwargs):
            return self.get(req)

    handlers = {
        'posts': PostsURLHandler,
        'videos': VideosURLHandler
    }