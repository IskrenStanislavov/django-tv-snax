import traceback, warnings, os, json

# from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import requires_csrf_token
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated
    )

# from rest_framework.parsers import JSONParser

from dejavu import Dejavu
from dejavu.recognize import FileRecognizer
from MySQLdb import ProgrammingError as mysql_ProgrammingError

from recognition.models import TVSong
from users.models import UserLog, EVENT_TYPES

warnings.filterwarnings("ignore")

def handle_uploaded_file(uploaded_file):
    path = default_storage.save('tmp/'+uploaded_file.name, ContentFile(uploaded_file.read()))
    tmp_file = os.path.join(settings.MEDIA_ROOT, path)
    return tmp_file

class myDejavu(Dejavu):
    def __init__(self):
        with open(settings.DJV_CONF) as f:
            super(myDejavu, self).__init__(json.load(f))
            f.close()
    def get_fingerprinted_songs(self):
        try:
            super(myDejavu, self).get_fingerprinted_songs()
        except mysql_ProgrammingError  as err:
            if err.args[0] == 1146: #"Table 'dejavu.songs' doesn't exist"
                self.db.setup()
            super(myDejavu, self).get_fingerprinted_songs()

from rest_framework import permissions
class CustomIsAdminUser(permissions.IsAdminUser):
    """
    Global permission check for blacklisted IPs.
    """

    def has_permission(self, request, view):
        ip_addr = request.META['REMOTE_ADDR']
        return request.user.is_staff or (ip_addr in settings.ADMINS_REMOTE_ADDRESSES)


djv = myDejavu()


@api_view(['POST',])
@permission_classes((CustomIsAdminUser, ))
def fingerprint(request):
    err_msgs=[]
    jsonResult = None
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        db_save_name = request.POST.get('name')
        if uploaded_file is None:
            err_msgs.append("No file uploaded")
            responseStatusCode = status.HTTP_400_BAD_REQUEST
        if db_save_name is None:
            err_msgs.append("Please name your upload")
            responseStatusCode = status.HTTP_400_BAD_REQUEST
        if db_save_name and uploaded_file:
            if uploaded_file.name[-3:] in settings.RECOGNIZABLE_EXTENSIONS:
                djv.get_fingerprinted_songs()
                if djv.is_fingerprinted(db_save_name):
                    message = "There is already an audio in the DB with this name: %s. If you want to update it please remove the old one"%(db_save_name)
                    err_msgs.append(message)
                    responseStatusCode = status.HTTP_400_BAD_REQUEST
                else:
                    fileName = handle_uploaded_file(uploaded_file)
                    try:
                        # audioId = djv.fingerprint_file(fileName, db_save_name)
                        audioId = djv.fingerprint_with_duration_check(fileName, minutes=3, song_name=db_save_name, processes=3)
                        #cleanup after fingerprinting
                        default_storage.delete(fileName)
                    except Exception,b:
                        # traceback.format_exception(Exception, b)
                        message = "Internal Server Error: %s"%str("<br/>".join(traceback.format_exc().splitlines()))
                        err_msgs.append(message)
                        responseStatusCode = status.HTTP_400_BAD_REQUEST
                    else:
                        jsonResult = {
                            "success":True,
                            "audioId": audioId
                            }
                        responseStatusCode=status.HTTP_201_CREATED
            else:
                err_msgs.append("Cannot recognise File Format")
                responseStatusCode = status.HTTP_400_BAD_REQUEST
    else:
        err_msgs.append("Invalid Request Method:%s"%(str(request.method)))
        responseStatusCode = status.HTTP_406_NOT_ACCEPTABLE
    jsonResult = jsonResult or {
        "success":False,
        "error":{
            "message": "wrong request parameters",
            "details":" ".join(err_msgs),
            "code":responseStatusCode
            }
        }

    return Response(jsonResult, status=status.HTTP_200_OK)


# 1. determine user
# 2. recognise the program
# 3. give points to user
        # user = getUserBySession(user_session)
        # if recognized:
        #     user.addBonusPoints(recognized.program.bonusPoints)

        # if not request.session.is_valid():
        #     err_msgs.append("Please sign in again.")
        #     responseStatusCode = status.HTTP_401_UNAUTHORIZED

@api_view(['POST',])
@permission_classes((IsAuthenticated, ))
def recognize(request):
    err_msgs=[]
    jsonResult = None
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')

        responseStatusCode = status.HTTP_200_OK
        if uploaded_file is None:
            err_msgs.append("No file uploaded")
            responseStatusCode = status.HTTP_404_NOT_FOUND
        elif uploaded_file.name[-3:] not in settings.RECOGNIZABLE_EXTENSIONS:
            err_msgs.append("Cannot recognise File Format")
            responseStatusCode = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

        # if user.isWatching():
        #     err_msgs.append("User trying to cheat")
        #     responseStatusCode = status.HTTP_300_MULTIPLE_CHOICES

        if responseStatusCode == status.HTTP_200_OK:
            fileName = handle_uploaded_file(uploaded_file)
            try:
                djv.get_fingerprinted_songs()
                result = djv.recognize(FileRecognizer, fileName)
            except Exception,b:
                err_msgs.append("Internal Server Error: %s"%str("<br/>".join(traceback.format_exc().splitlines())))
                responseStatusCode = status.HTTP_500_INTERNAL_SERVER_ERROR
            else:
                # print(result)
                if (not result) or ( result.get("confidence") < settings.RECOGNITION_MINIMUM ):
                    responseStatusCode = status.HTTP_404_NOT_FOUND
                    err_msgs.append("Recognition failed")
                else:
                    song = TVSong.objects.get(pk=result.get("audio_id"))
                    try:
                        song.programs
                    except Exception:# django custom exception: RelatedObjectDoesNotExist:
                        err_msgs.append("No program for the recognized song:%s"%(song.name))
                    else:
                        if (not song.programs.isActive()):
                            err_msgs.append("Program is closed now, please check the program schedule")
                        else:
                            UserLog.objects.create(
                                user=request.user,
                                eventType=EVENT_TYPES.GET,
                                details=song.programs.name,
                                points=song.programs.points).save()
                            request.user.setWatching(song.programs)
                            jsonResult = {
                                "success": True,
                                "result": {
                                    "recognized": True,
                                    "audioId": song.audio_id,
                                    "programId": song.programs.id,
                                    "confidence": result.get("confidence"),
                                    "points": song.programs.points, # user receive them
                                    }
                                }

            #cleanup after recognition
            fileName and default_storage.delete(fileName)
    else:
        err_msgs.append("Invalid Request Method:%s"%(str(request.method)))
        responseStatusCode = status.HTTP_400_BAD_REQUEST
    jsonResult = jsonResult or {
        "success":False,
        "error":{
            "message":" ".join(err_msgs),
            "code":responseStatusCode
            }
        }
    return Response(jsonResult, status=status.HTTP_200_OK)
