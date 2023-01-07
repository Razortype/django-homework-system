from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),
    path('', include('users.urls')),

    ##################### Handler Test URLs #####################
    path('handler404', views.handler404Test, name="handler404Test"),
    path('handler500', views.handler500Test, name="handler500Test")
]


handler404 = 'homework_project.views.handler404'
handler500 = 'homework_project.views.handler500'