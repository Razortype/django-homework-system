from django.urls import path
from . import views

urlpatterns = [
    path('videos', views.VideoList.as_view(), name="video_list"),
    path('videos/<str:category>', views.VideoListByType.as_view(), name="video_list_by_type")
]