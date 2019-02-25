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

from prizes.models import Kind as Prizes, UserPrize
from users.models import UserLog, EVENT_TYPES
from prizes.serializers import PrizesSerializer

CustomError = {"success":False, "error":{"message":"Wrong request data", "details":"", "code":100}}
PointsError = {"success":False, "error":{"message":"You do not have enough Points for this Prize.", "details":"", "code":100}}
InactiveError = {"success":False, "error":{"message":"The Prize you chose is not available now/anymore.", "details":"", "code":100}}
BadParamsError = {"success":False, "error":{"message":"Wrong request data", "details":"Missing 'prizeId' parameter in the request data.", "code":100}}
AlreadyBoughtError = {"success":False, "error":{"message":"Already bought.", "details":"User has allready bought that Price.", "code":100}}



@api_view(['GET'])
@permission_classes((
    IsAuthenticated,
))
def list(request):
    if request.method == 'GET':
        prizes = Prizes.objects.exclude(activeTo__lt=timezone.now())
        serializer = PrizesSerializer(request.user, prizes, many=True)
        serializer.is_valid()
        result = {"success":True, "prizes":serializer.data}
    else:
        result = CustomError
    return Response(result)

@api_view(['POST'])
@permission_classes((
    IsAuthenticated,
))
def take(request):
    if not request.method == 'POST':
        return Response(CustomError)

    wantedPrize = request.data.get("prizeId")
    if wantedPrize is None:
        return Response(BadParamsError)
    try:
        prizeKind = Prizes.objects.get(pk=int(wantedPrize))
    except Prizes.DoesNotExist:
        return Response(InactiveError)
    if prizeKind.boughtByUser(request.user):
        return Response(AlreadyBoughtError)
    if not prizeKind.isActive():
        return Response(InactiveError)

    try:
        UserPrize.objects.create(user=request.user, prize=prizeKind).save()
        request.user.takePoints(prizeKind.points)
    except ValueError,e:
        if "points" in str(e):
            result = PointsError
        else:
            result = {"success":False, "message":"Wrong request data.", "details":str(e), "code":100}
    except Exception,e:
        result = {"success":False, "message":"Wrong request data.", "details":str(e), "code":100}
    else:
        UserLog.objects.create(
            user=request.user,
            eventType=EVENT_TYPES.PAY,
            details=prizeKind.name,
            points=-prizeKind.points).save()
        result = {"success":True, "user":{"points":request.user.points}}
    return Response(result)
        
