from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

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
