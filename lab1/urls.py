"""lab1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views

urlpatterns = [
     url('^', include('django.contrib.auth.urls')),
     url(r'^accounts/login/$', views.login, name='login'),
     url(r'login/$', views.login, name='login'),
#    url(r'^accounts/auth/$', 'django_test.views.auth_view'),
     url(r'^logout/$', views.logout, name='logout', kwargs={'next_page': 'urlexpander'}),
#    url(r'^accounts/loggedin/$', 'django_test.views.loggedin'),
#    url(r'^accounts/invalid/$', 'django_test.views.invalid_ilogin'),
    url(r'^admin/', admin.site.urls),
    url(r'^urlexpander/', include('urlexpander.urls')),
]

