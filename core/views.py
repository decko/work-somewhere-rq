from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import Task


@api_view(['GET'])
def task_view(request, job_id=None):
    """
    Endpoint to retrieve a specific task.


    Parameters
    ----------
    job_id : uuid, optional
        The job_id to retrieve the task
    """

    task = get_object_or_404(Task, job_id=job_id)

    response = {
        'job_id': task.get_absolute_url(),
        'status': task.status,
        'data': task.data,
        'result': task.result
    }

    return Response(data=response, status=200)
