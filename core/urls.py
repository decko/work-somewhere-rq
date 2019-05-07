from django.urls import path

from .views import return200Ok


app_name = 'core'

urlpatterns = [
    path('task/', return200Ok, name='task-list'),
]
