from django.urls import path

from .views import bill_view


app_name = 'bills'

urlpatterns = [
    path('bills',
         bill_view)
]
