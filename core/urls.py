from django.urls import path

from .views import TaskRetrieveAPIView, task_view


app_name = 'core'

urlpatterns = [
    path('task/<uuid:job_id>', TaskRetrieveAPIView.as_view(), name='task-detail'),
    path('task/', task_view, name='task-list'),
]
