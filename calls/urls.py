from django.urls import path

from .views import return200Ok


app_name = 'calls'

urlpatterns = [
    path('registry/', return200Ok, name='registry-list'),
]


