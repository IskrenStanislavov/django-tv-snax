from django.conf.urls import url
from recognition import workers
urlpatterns = [
	url(r'^recognize$', workers.recognize),
	url(r'^recognise$', workers.recognize),
	url(r'^audio/fingerprint$', workers.fingerprint),
	url(r'^recognize/$', workers.recognize),
	url(r'^recognise/$', workers.recognize),
	url(r'^audio/fingerprint/$', workers.fingerprint),
]