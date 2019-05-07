from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def registry_saver(request):

    if request.method == 'GET':
        return Response(status=200)

    response = {
        'job_id': 'job_id',
        'data': request.data
    }

    return Response(data=response, status=201)
