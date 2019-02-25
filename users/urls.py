
from django.conf.urls import include, url
from users import views
urlpatterns = [
    url(r'^auth/register$', views.create_auth),#
	url(r'^users/profile$', views.UserViewSet.as_view({'get': 'retrieve', 'post': 'update'})),
    url(r'^users/log$', views.UserLogSet.as_view({'get': 'list'})),#
    url(r'^auth/login$', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^auth/logout$', views.logout),#
    url(r'^auth/register/$', views.create_auth),#
	url(r'^users/profile/$', views.UserViewSet.as_view({'get': 'retrieve', 'post': 'update'})),
    url(r'^users/log/$', views.UserLogSet.as_view({'get': 'list'})),#
    url(r'^auth/login/$', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^auth/logout/$', views.logout),#
]