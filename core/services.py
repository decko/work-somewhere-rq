from abc import ABC, abstractmethod

from rq import get_current_job

from django_rq import enqueue

from .models import Task


class ServiceAbstractClass(ABC):
    """
    This Abstract Service Class defines a template to process messages
    on Telephone application.

    message : dict
        The message to be processed.
    """

    trigger = None
    queue = None
    validation_class = None

    def __init__(self, *args, **kwargs):
        self.message = kwargs.get('message', None)
        self.job_id = kwargs.get('job_id', None)
        self.result = None
        self.is_valid = None

        if not self.trigger or not isinstance(self.trigger, str):
            raise Exception("A trigger must be a string and it is needed to accept any task.")

        if not self.queue or not isinstance(self.queue, str):
            raise Exception("A queue must be a string and it is needed to propagate the results.")

    @abstractmethod
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
                'service': self.__class__.__name__
            }
        )

        task.status = 'STARTED'
        task.save()

        self.task = task
        return task

    @abstractmethod
    def obtainMessage(self):
        """
        Obtains the data needed to be processed.

        self.message could contain any information used to obtain the data
        or could be the date itself.
        """
        pass

    @abstractmethod
    def validateMessage(self):
        """
        Validates the message received.

        Validate the message received using validation class from
        validation_class attribute.
        """
        pass

    @abstractmethod
    def transformMessage(self):
        """
        Transform the validated message into something else needed.

        Transform the message to a new format used by other methods.
        """
        pass

    @abstractmethod
    def persistData(self):
        """
        Persist the data into a storage.

        Persist the data into a storage like a Django Model or something else.
        """
        pass

    @abstractmethod
    def propagateResult(self):
        """
        Propagate the result into a defined queue.

        Propagate the result into a defined queue to be processed by other
        Services.
        """

        enqueue('core.tasks.dispatch', self.result, self.queue)

    @abstractmethod
    def finishTask(self, failed=None):
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

        if failed:
            task.status = 'FAILED'

        task.save()

        return task

    def process(self):
        """
        Run all the methods to process a message and propagate the result.
        """

        self.startTask()
        self.obtainMessage()
        self.validateMessage()
        self.transformMessage()
        self.persistData()
        self.finishTask()
        self.propagateResult()
