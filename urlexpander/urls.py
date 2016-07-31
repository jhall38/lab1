from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<url_pk>[0-9]+)/$', views.detail, name='detail'),
	url(r'^expand/$', views.expand_url, name='expand_url'),
	url(r'^(?P<url_pk>[0-9]+)/delete/$', views.delete, name='delete'),
]
