from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),
    path('', include('users.urls')),
    path('', include('videos.urls')),

    ##################### Handler Test URLs #####################
    path('handler403', views.handler403Test, name="handler403Test"),
    path('handler404', views.handler404Test, name="handler404Test"),
    path('handler500', views.handler500Test, name="handler500Test"),

    path('server-commands', views.ServerController.as_view(), name="sw_controller"),
]


handler403 = 'homework_project.views.handler403'
handler404 = 'homework_project.views.handler404'
handler500 = 'homework_project.views.handler500'