from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer


class TaskRetrieveAPIView(RetrieveAPIView):
    """
    Retrieve a single Task instance.

    job_id: uuid
    The identifier to retrieve the Task.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'job_id'


class TaskListAPIView(ListAPIView):
    """
    Endpoint to retrieve all tasks.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
