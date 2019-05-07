from django.urls import path

from .views import task_view


app_name = 'core'

urlpatterns = [
    path('task/', task_view, name='task-list'),
]
