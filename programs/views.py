from django.utils import timezone
from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated
    )

from programs.models import Pr as Programs
from programs.serializers import ProgramsSerializer

CustomError = JSONRenderer().render({"success":False, "error":{"message":"Wrong request data", "code":100}})

class CustomResponse(HttpResponse):
    def __init__(self, data, response_data_name=None, *a, **kwargs):
        kwargs['content_type'] = 'application/json'
        if "response_data_name" is not None:
            result = {"success":True}
            result[response_data_name] = data
            content = JSONRenderer().render(result)

            super(CustomResponse, self).__init__(content, **kwargs)
        else:
            super(CustomResponse, self).__init__(CustomError, **kwargs)

class ErrorResponse(HttpResponse):
    def __init__(self,*a,**kw):
        kwargs['content_type'] = 'application/json'
        super(ErrorResponse, self).__init__(CustomError, **kw)

@api_view(['GET'])
@permission_classes((
    IsAuthenticated,
))
def programs_list(request):
    if request.method == 'GET':
        programs = Programs.objects.exclude(activeTo__lt=timezone.now())
        serializer = ProgramsSerializer(programs, many=True)
        return CustomResponse(serializer.data, response_data_name="program")
    else:
        return ErrorResponse()
