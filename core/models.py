from django.db import models
from django.urls import reverse_lazy

from django.contrib.postgres.fields import JSONField


class Task(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=(
            ('queued', 'QUEUED'), ('started', 'STARTED'), ('done', 'DONE')
        ),
        default='queued',
        max_length=7
    )
    data = JSONField()
    job_id = models.UUIDField(null=True, blank=True)
    result = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse_lazy('core:task-detail', kwargs={'job_id': self.job_id})
