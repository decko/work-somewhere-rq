from django.db import models
from django.urls import reverse_lazy


class Task(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=(
            ('queued', 'QUEUED'), ('started', 'STARTED'), ('done', 'DONE'),
            ('failed', 'FAILED')
        ),
        default='queued',
        max_length=7
    )
    data = models.TextField()
    job_id = models.UUIDField(null=True, blank=True)
    service = models.CharField(max_length=200, null=True, blank=True)
    result = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse_lazy('core:task-detail', kwargs={'job_id': self.job_id})
