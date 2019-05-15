from rq import get_current_job

from django_rq import job, get_queue

from core.models import Task

from .serializers import RegistrySerializer

from .models import Call
from .models import Registry


@job('registry-q')
def registry_validation(data):
    job = get_current_job()

    task = Task()
    task.status = 'STARTED'
    task.job_id = job.id
    task.data = data
    task.save()

    registry = RegistrySerializer(data=data)

    if registry.is_valid():
        registry_queue = get_queue('registry-q')
        call_queue = get_queue('call-q')

        registry_queue.enqueue(registry_saver, registry.data, job.id)
        call_queue.enqueue(call_saver, registry.data)
    else:
        task.status = 'DONE'
        task.result = registry.errors
        task.save()

    return True


@job('registry-q')
def registry_saver(data, job_id):
    """
    Receives validated data and save it to a new Registry instance.
    Also, update the Task instance with 'DONE' status and the result.

    data : dict
        Message containing data to be persisted on Registry model

    job_id : uuid
        UUID to find the Task instance to update status
    """

    registry = Registry.objects.create(**data)

    task = Task.objects.get(job_id=job_id)
    task.result = registry.get_absolute_url()
    task.status = 'DONE'
    task.save()

    return True


@job('call-q')
def call_saver(data):
    """
    Receives validated data, transform and update a Call instance or
    create a new one if a previous isn't found. Update the Task instance
    with 'DONE' status and the result.

    data : dict
        Message containing data to be persisted on Call model
    """

    job = get_current_job()

    task = Task()
    task.status = 'STARTED'
    task.job_id = job.id
    task.data = data
    task.save()

    call_data = {
        'call_id': data.get('call_id')
    }
    if data.get('type') == 'start':
        call_data['start_timestamp'] = data.get('timestamp')
        call_data['source'] = data.get('source')
        call_data['destination'] = data.get('destination')
    else:
        call_data['stop_timestamp'] = data.get('timestamp')

    call, created = Call.objects.update_or_create(
        call_id=call_data.get('call_id'),
        defaults=call_data
    )

    task.result = call.get_absolute_url()
    task.status = 'DONE'
    task.save()

    return True
