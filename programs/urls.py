from django.conf.urls import url
from programs import views
urlpatterns = [
	url(r'^program/list$', views.programs_list),
	url(r'^program/list/$', views.programs_list),
]