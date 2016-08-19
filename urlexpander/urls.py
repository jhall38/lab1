from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from .views import (
	URLCreateUpdateAPIView
)
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<url_pk>[0-9]+)/$', views.detail, name='detail'),
	url(r'^expand/$', views.expand_url, name='expand_url'),
	url(r'^(?P<url_pk>[0-9]+)/delete/$', views.delete, name='delete'),
	url(r'^api/urls/$', views.url_list, name='url_list'),
	#url(r'^api/urls/create$', URLCreateUpdateAPIView.as_view(), name='create'),
	url(r'^api/urls/(?P<pk>[0-9]+)/$', views.url_detail, name='url_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
