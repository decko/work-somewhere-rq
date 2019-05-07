from django.urls import path

from .views import registry_saver


app_name = 'calls'

urlpatterns = [
    path('registry/', registry_saver, name='registry-list'),
]


