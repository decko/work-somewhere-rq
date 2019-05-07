from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def task_view(request, task_id):

    return Response(status=200)
