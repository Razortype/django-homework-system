from django.urls import path
from . import views

urlpatterns = [
    path('videos', views.VideoList.as_view(), name="video_list"),
]