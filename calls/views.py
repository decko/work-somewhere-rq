from uuid import uuid4

from django.urls import reverse_lazy

from django_rq import get_queue

from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from .serializers import RegistrySerializer
from .serializers import CallSerializer
from .models import Registry
from .models import Call


class RegistryListCreateAPIView(ListCreateAPIView):
    queryset = Registry.objects.all()
    serializer_class = RegistrySerializer

    def post(self, request):
        queue = get_queue('registry-q')
        job = queue.enqueue('calls.tasks.registry_validation', data=request.data)

        task_url = reverse_lazy('core:task-detail', kwargs={'job_id': job.id})

        data = {
            'job_id': task_url,
            'data': request.data
        }

        return Response(data=data, status=201)


class RegistryRetrieveAPIView(RetrieveAPIView):
    queryset = Registry.objects.all()
    serializer_class = RegistrySerializer


class CallListAPIView(ListAPIView):
    """
    Retrieve all consolidated(with start and stop timestamps) calls.
    """

    queryset = Call.consolidated.all()
    serializer_class = CallSerializer


class CallRetrieveAPIView(RetrieveAPIView):
    queryset = Call.consolidated.all()
    serializer_class = CallSerializer
    lookup_field = 'call_id'


@api_view(['GET', 'POST'])
def registry_view(request, registry_id=None):

    if request.method == 'GET':
        return Response(status=200)


    response = {
        'job_id': task_url,
        'data': request.data
    }

    return Response(data=response, status=201)
