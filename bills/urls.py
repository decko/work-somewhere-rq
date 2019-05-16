from django.urls import path

from .views import bill_view


app_name = 'bills'

urlpatterns = [
    path('bills/<int:subscriber>',
         bill_view,
         name='bill-detail'),

    path('bills',
         bill_view,
         name='bill-list'),
]
