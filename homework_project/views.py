from django.http import HttpResponse
from django.shortcuts import render

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
def handler404Test(request):
    content = {
        'title': 'Web | Sayfa Bulunamadı',
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