from django.contrib import admin
from django.urls import path, re_path, include

from django.conf import settings

from . import views
from . utils import get_json_dot_seperated, scan_url_file

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),

    ##################### Handler Test URLs #####################
    path('handler403', views.handler403Test, name="handler403Test"),
    path('handler404', views.handler404Test, name="handler404Test"),
    path('handler500', views.handler500Test, name="handler500Test"),

    path('server-commands', views.ServerController.as_view(), name="sw_controller"),
]


handler403 = 'homework_project.views.handler403'
handler404 = 'homework_project.views.handler404'
handler500 = 'homework_project.views.handler500'

data = get_json_dot_seperated(settings.URL_CONFIG_DIR)
for key, val in data.maintenance.items():
    if not val:
        urlpatterns.append(path('', include(f'{key}.urls')))
    else:
        pairs = scan_url_file(key)
        for pattern, name in pairs:
            urlpatterns.append(re_path(pattern, views.ApplicationHandler.handlers.get(key).as_view(), name=name))