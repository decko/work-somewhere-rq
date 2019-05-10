from uuid import uuid4

from django.urls import reverse_lazy

from django_rq import get_queue

from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from .serializers import RegistrySerializer
from .models import Registry


class RegistryListCreateAPIView(ListCreateAPIView):
    queryset = Registry.objects.all()
    serializer_class = RegistrySerializer

    def post(self, request):
        queue = get_queue('registry-q')
        job = queue.enqueue('calls.tasks.registry_saver', data=request.data)

        task_url = reverse_lazy('core:task-detail', kwargs={'job_id': job.id})

        data = {
            'job_id': task_url,
            'data': request.data
        }

        return Response(data=data, status=201)


class RegistryRetrieveAPIView(RetrieveAPIView):
    queryset = Registry.objects.all()
    serializer_class = RegistrySerializer


@api_view(['GET', 'POST'])
def registry_view(request, registry_id=None):

    if request.method == 'GET':
        return Response(status=200)


    response = {
        'job_id': task_url,
        'data': request.data
    }

    return Response(data=response, status=201)
