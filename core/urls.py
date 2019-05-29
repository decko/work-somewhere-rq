from django.urls import path

from .views import TaskListAPIView
from .views import TaskRetrieveAPIView


app_name = 'core'

urlpatterns = [
    path('task/<uuid:job_id>', TaskRetrieveAPIView.as_view(), name='task-detail'),
    path('task/', TaskListAPIView.as_view(), name='task-list'),
]
