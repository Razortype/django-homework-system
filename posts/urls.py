from django.urls import path
from . import views

urlpatterns = [
    path('homeworks', views.HomeworkList.as_view(), name="hw_list"),
    path('homeworks/<str:category>', views.HomeworkListByType.as_view(), name="hw_list_by_category"),
    path('homeworks/id/<int:_id>/detail', views.HomeworkDetailById.as_view(), name="hw_detail_by_id"),

    path('homeworks/id/<int:_id>/post/new', views.HomeworkPostNew.as_view(), name="post_new"),
    path('homeworks/id/<int:homework_id>/posts/<int:post_id>/post-update', views.HomeworkPostUpdate.as_view(), name="post_update"),
    path('homeworks/id/<int:homework_id>/posts/<int:post_id>/post-delete', views.HomeworkPostDelete.as_view(), name="post_delete")
]