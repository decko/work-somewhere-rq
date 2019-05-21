from rq import get_current_job

from core.services import ServiceAbstractClass
from core.models import Task


class RegistryService(ServiceAbstractClass):
    """
    RegistryService is a service responsible for new registries processing.
    """

    trigger = 'registry-service'
    queue = 'registry-service-done'

    def startTask(self):
        """
        Start the job process.

        Start the job process persisting a Task instance. If there is
        a job instance, find the correspondent Task instance or create a
        new one if it wasn't found.
        """
        job_id = self.job_id
        if not job_id:
            job_id = get_current_job().id

        task, created = Task.objects.get_or_create(
            job_id=job_id,
            defaults={
                'status': 'QUEUED',
                'job_id': job_id,
                'data': self.message,
            }
        )

        task.status = 'STARTED'
        task.save()

        self.task = task
        return task

    def obtainMessage(self):
        pass

    def validateMessage(self):
        pass

    def transformMessage(self):
        pass

    def persistData(self):
        pass

    def propagateResult(self):
        pass

    def finishTask(self):
        """
        Finish the job process.

        Set the Task result attribute to self.result, set the status to 'DONE'
        and save Task instance.
        """
        result = self.result
        task = self.task

        if result:
            task.result = result

        task.status = 'DONE'
        task.save()

        return task
