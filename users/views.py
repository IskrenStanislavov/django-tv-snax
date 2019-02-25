
from django.contrib.auth import get_user_model
from rest_framework_jwt.serializers import JSONWebTokenSerializer

from users.models import UserLog
from users.serializers import UserProfileSerializer
from users.serializers import UserLogSerializer
from rest_framework import (
    status,
    viewsets,
)

from rest_framework.response import Response

from rest_framework.decorators import (
    api_view,
    permission_classes,
    list_route,
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

class UserLogSet(viewsets.ModelViewSet):
    queryset = UserLog.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserLogSerializer
    lookup_field = "id"
    def get_object(self):
        return self.request.user.events

    def list(self, request, pk=None):
        try:
            result = {
                "success": True,
                "log":super(UserLogSet, self).list(request).data,
                }
        except ValueError, err:
            result = {"message":"Internal Server Error", "success":False, "details":str(err)}
        return Response(result)

class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer
    lookup_field = "pk"
    def get_object(self):
        return self.request.user

    def retrieve(self, request, pk=None):
        try:
            result = {
                "success": True,
                "user":super(UserViewSet, self).retrieve(request).data,
                }
        except Exception, err:
            result = {"message":"err", "success":False, "details":err.details}
        return Response(result)

    def update(self, request, pk=None):
        response = super(UserViewSet, self).update(request, pk=request.user.id, partial=True)
        result = {"success": True}
        # result["user"] = response.data
        return Response(result)

# http://stackoverflow.com/a/17749567
@api_view(['POST'])
@permission_classes((
    AllowAny,
))
def create_auth(request):
    serialized = UserProfileSerializer(data=request.data)
    jwt = JSONWebTokenSerializer(data=request.data)
    data = jwt.is_valid()
    if serialized.is_valid():
        serialized.save()
        result = {"success":True, "sessionId":jwt.validate(request.data)["token"]}
        code = status.HTTP_201_CREATED
    else:
        code = status.HTTP_400_BAD_REQUEST
        result = {"success": False, "message": "Wrong request data", "details":str(serialized._errors), "code":code}
    return Response(result, status=code)

@api_view(['POST'])
@permission_classes((
    IsAuthenticated,
))
def logout(request):
    return Response({"success":True}, status=status.HTTP_201_CREATED)
