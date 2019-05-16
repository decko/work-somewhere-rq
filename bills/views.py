from datetime import date

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def bill_view(request, subscriber=None):

    if not subscriber:
        return Response(status=403)

    today = date.today()
    latest_period = today.replace(
        year=today.year if today.month > 1 else today.year - 1,
        month=today.month - 1 if today.month > 1 else 12,
        day=1).strftime('%h/%Y')

    data = {
        'subscriber': subscriber,
        'period': latest_period,
    }

    return Response(data=data, status=200)
