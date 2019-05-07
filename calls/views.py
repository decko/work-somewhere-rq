from uuid import uuid4

from django.urls import reverse_lazy

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def registry_saver(request):

    if request.method == 'GET':
        return Response(status=200)

    task_url = reverse_lazy('core:task-detail', kwargs={'task_id': uuid4()})

    response = {
        'job_id': task_url,
        'data': request.data
    }

    return Response(data=response, status=201)
