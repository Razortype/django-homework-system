from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from django.contrib import messages 
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin

from django.conf import settings
from .utils import get_commands, get_maintenance_commands, run_sh, get_json_dot_seperated, read_json_data, dump_json_data

from users.models import Person

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

        user = req.user

        content = {
            'person': Person.objects.get(pk=user.id),
            'commands': get_commands().keys(),
            'maintenance': get_json_dot_seperated(settings.URL_CONFIG_DIR).maintenance,
            'style_file': 'partials/css/commands.css',
            'js_files': [
                'partials/js/commands.js',
                'partials/js/_navbar.js',
            ]
        }
        return HttpResponse(render(req, 'commands.html', content))

    def post(self, req, *args, **kwargs):
        
        if not req.user.is_superuser and not isinstance(req.user, AnonymousUser):
            messages.warning(req, "Bu sayfada işlem izininiz bulunmamaktadır")
            return HttpResponseRedirect('/')

        maintenance_commands = get_maintenance_commands(settings.URL_CONFIG_DIR)
        for m_command in maintenance_commands:
            if m_command in req.POST:
                app_name = m_command.split("_")[0]
                data = read_json_data(settings.URL_CONFIG_DIR)
                data["maintenance"][app_name] = not data["maintenance"][app_name]
                dump_json_data(settings.URL_CONFIG_DIR, data)
                run_sh("reload_server.sh")

                messages.success(req, "Uygulama bakım durumu başarıyla değiştirildi")
                return HttpResponseRedirect('/server-commands')

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