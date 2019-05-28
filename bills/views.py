import calendar
from datetime import date

from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .serializers import BillSerializer
from .models import Bill


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

    month_as_int = {abbr: month for month, abbr in
                    enumerate(calendar.month_abbr)}.get(month_period)

    calls = [call for call in Bill.objects.filter(subscriber=subscriber)
             .filter(stop_timestamp__iso_year=year_period)
             .filter(stop_timestamp__month=month_as_int)]

    if not calls:
        raise NotFound(detail='No result was returned from your query.')

    data = {
        'subscriber': subscriber,
        'period': period,
        'calls': calls,
    }

    serializer = BillSerializer(data)

    return Response(data=serializer.data, status=200)
