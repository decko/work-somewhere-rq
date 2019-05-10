from rq import get_current_job

from django_rq import job

from core.models import Task

from .serializers import RegistrySerializer


@job('registry-q')
def registry_saver(data):
    job = get_current_job()
    
    task = Task()
    task.status = 'STARTED'
    task.job_id = job.id
    task.data = data
    task.save()

    registry = RegistrySerializer(data=data)

    if registry.is_valid():
        instance = registry.save()
        task.result = instance.get_absolute_url()
    else:
        task.result = registry.errors

    task.status = 'DONE'
    task.save()
    return task.result
