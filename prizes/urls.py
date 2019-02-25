from django.conf.urls import url
from prizes import views
urlpatterns = [
	url(r'^prizes/list$', views.list),
	url(r'^prizes/take$', views.take),
	url(r'^prizes/list/$', views.list),
	url(r'^prizes/take/$', views.take),
]