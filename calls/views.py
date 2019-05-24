from django.urls import reverse_lazy

from django_rq import enqueue

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
        service = enqueue('core.tasks.dispatch',
                          message=request.data,
                          trigger='registry-service')

        task_url = reverse_lazy('core:task-detail',
                                kwargs={'job_id': service.id})

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
    """
    Retrieve a specific consolidated call using call_id.
    """
    queryset = Call.consolidated.all()
    serializer_class = CallSerializer
    lookup_field = 'call_id'
