from rq import get_current_job

from django_rq import job

from core.models import Task

from .serializers import RegistrySerializer

from .models import Call


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

        call_data = {
            'call_id': instance.call_id,
        }
        if instance.type == 'start':
            call_data['start_timestamp'] = instance.timestamp
            call_data['source'] = instance.source
            call_data['destination'] = instance.destination
        else:
            call_data['stop_timestamp'] = instance.timestamp

        obj, created = Call.objects.update_or_create(
            call_id=instance.call_id,
            defaults=call_data
        )
        task.result = instance.get_absolute_url()
    else:
        task.result = registry.errors

    task.status = 'DONE'
    task.save()
    return task.result
