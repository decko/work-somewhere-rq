import calendar
from datetime import date

from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from .serializers import BillSerializer
from .models import Bill


@api_view(['GET'])
def bill_view(request, subscriber=None, month_period=None, year_period=None):
    """
    Function Based View used to retrieve Bill data for a subscriber.

    subscriber : int, str
        The subscriber number required to retrieve a bill. Not optional.

    month_period : str, optional
        The name of the month abbreviated to 3 characters format,
        used to filter a bill from a subscriber. e.g. Jan, Feb, Mar...

    year_period : int, optional
        The year period in ISO format(4 digits), used to filter a bill
        from a subscriber. e.g. 2017, 2018, 2019...
    """

    today = date.today()
    current_month = today.month
    current_year = today.year

    if not subscriber:
        return Response(status=403)

    if not year_period:
        year_period = current_year

    if not month_period:
        month_period = today.replace(
            year=today.year if today.month > 1 else today.year - 1,
            month=today.month - 1 if today.month > 1 else 12,
            day=1).strftime('%h')

    month_as_int = {abbr.lower(): month for month, abbr in
                    enumerate(calendar.month_abbr)}.get(month_period.lower(), 0)

    if month_as_int >= current_month\
       and year_period >= current_year:
        raise ParseError(detail=('It\'s only possible to get a telephone bill'
                                 ' after the reference period has ended.'))

    period = f"{month_period}/{year_period}"

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
