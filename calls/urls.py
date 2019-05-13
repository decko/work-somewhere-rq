from django.urls import path

from .views import RegistryRetrieveAPIView
from .views import RegistryListCreateAPIView

from .views import registry_view as call_view


app_name = 'calls'

urlpatterns = [
    path('registry/<int:pk>',
         RegistryRetrieveAPIView.as_view(),
         name='registry-detail'),

    path('registry/',
         RegistryListCreateAPIView.as_view(),
         name='registry-list'),

    path('calls/',
         call_view,
         name='call-list'),
]
