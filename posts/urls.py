from django.urls import path
from . import views

urlpatterns = [
    path('homeworks', views.HomeworkList.as_view(), name="hw_list"),
    path('homeworks/<str:category>', views.HomeworkListByType.as_view(), name="hw_list_by_category"),
    path('homeworks/id/<int:id>', views.HomeworkDetailById.as_view(), name="hw_detail_by_id"),
]