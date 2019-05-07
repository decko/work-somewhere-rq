from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def registry_saver(request, **kwargs):

    return Response(status=200)
