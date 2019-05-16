from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def bill_view(request, subscriber=None):

    if not subscriber:
        return Response(status=403)

    data = {'subscriber', 'period'}

    return Response(data=data, status=200)
