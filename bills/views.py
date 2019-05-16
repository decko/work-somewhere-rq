from datetime import date

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def bill_view(request, subscriber=None, month_period=None, year_period=None):

    if not subscriber:
        return Response(status=403)

    if not year_period:
        year_period = date.today().year

    if not month_period:
        today = date.today()
        month_period = today.replace(
            year=today.year if today.month > 1 else today.year - 1,
            month=today.month - 1 if today.month > 1 else 12,
            day=1).strftime('%h')

    period = f"{month_period}/{year_period}"

    data = {
        'subscriber': subscriber,
        'period': period,
        'calls': [],
    }

    return Response(data=data, status=200)
