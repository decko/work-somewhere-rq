from django.db import models


class ConsolidatedCallManager(models.Manager):
    """
    Manager to query only call with start and stop timestamp.
    """

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(start_timestamp__isnull=False,
                                   stop_timestamp__isnull=False)
        return queryset

