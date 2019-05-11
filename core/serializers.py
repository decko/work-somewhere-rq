from rest_framework.serializers import ModelSerializer

from .models import Task


class TaskSerializer(ModelSerializer):

    class Meta:
        model = Task
        fields = ('job_id', 'status', 'data', 'result')
