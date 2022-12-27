from django.urls import path
from . import views

urlpatterns = [
    path('homeworks', views.HomeworkList.as_view(), name="homework list"),
    path('homeworks/<str:type_name>', views.HomeworkListByType.as_view(), name="homework list by type"),
    path('homeworks/id/<int:id>', views.HomeworkDetailById.as_view(), name="homework detail by id"),
]