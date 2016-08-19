from django.shortcuts import render, get_object_or_404
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from selenium import webdriver
from django.core.files.base import ContentFile
import uuid
import os
from django.core.files import File
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ratelimit.decorators import ratelimit
from urlexpander.serializers import URLDetailSerializer, URLCreateUpdateSerializer, ArchivedSerializer
from rest_framework import generics
from rest_framework.generics import (
	CreateAPIView,
	DestroyAPIView,
	ListAPIView,
)
from .models import URL, Archived

@login_required(login_url='/login/')
def index(request):
	all_urls = URL.objects.all()
	return render(request, 'urlexpander/index.html', {'all_urls' : all_urls})

@login_required(login_url='/login/')
def detail(request, url_pk):
	this_url = get_object_or_404(URL, pk=url_pk)
	return render(request, 'urlexpander/detail.html', {'this_url' : this_url})

@login_required(login_url='/login/')
def expand_url(request):
	shortend_url = request.POST['shortend_url']
	new_url = URL()
	try:
		html = requests.get(shortend_url)
		print(html.status_code)
		if html.status_code == 200:
			soup = BeautifulSoup(html.content)
			new_url.page_title = soup.html.head.title.contents[0]
		else:
			new_url.page_title = "Not availible"
		new_url.shortend_url = shortend_url
		new_url.expanded_url = html.url
		new_url.status = html.status_code
		new_url.save()
		request_url = "http://archive.org/wayback/available?url=" + new_url.expanded_url
		r = requests.get(request_url).json()["archived_snapshots"]
		if r:
			new_archived = Archived()
			new_archived.archived_url = r["closest"]["url"]
			timestamp = r["closest"]["timestamp"]
			to_store = timestamp[:4] + "-" + timestamp[4:6] + "-" + timestamp[6:8] + " " + timestamp[8:10] + ":" + timestamp[10:12] + ":" + timestamp[12:14]
			new_archived.timestamp = to_store
			new_archived.save()
			new_url.archived = new_archived
			driver = webdriver.PhantomJS()
			driver.set_window_size(1024, 768)
			driver.get(new_archived.archived_url)
			temp = 'website_img_' + str(new_url.id) + '.png'
			driver.save_screenshot('urlexpander/media/' + temp)
			img = File(open('urlexpander/media/' + temp, 'rb'))
			new_url.website_img.save(temp, img, save=True)
			new_url.save()
			os.remove('urlexpander/media/' + temp)
			return render(request, 'urlexpander/detail.html', {'this_url' : new_url, 'this_archive' : new_archived})

		else:
			return render(request, 'urlexpander/detail.html', {'this_url' : new_url})		
	except requests.exceptions.RequestException as e: 
		return render(request, 'urlexpander/error.html', {'e' : e})

@login_required
def delete(request, url_pk):
	this_url = get_object_or_404(URL, pk=url_pk)
	this_url.website_img.delete()
	this_url.delete()
	return render(request, 'urlexpander/index.html', {'all_urls' : URL.objects.all()})

@login_required(login_url='/login/')
@ratelimit(key='ip', rate='10/m', block=True)
@api_view(['GET', 'POST'])
def url_list(request, format=None):
	if request.method == 'GET':
		books = Book.objects.all()
		serializer = BookSerializer(books, many=True)
		return Response(serializer.data)
	elif request.method == 'POST':
		serializer = BookSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@login_required(login_url='/login/')
@ratelimit(key='ip', rate='10/m', block=True)
@api_view(['GET', 'DELETE'])
def url_detail(request, pk, format=None):
        try:
                url = URL.objects.get(pk=pk)
		if request.method == 'DELETE':
			this_url = get_object_or_404(URL, pk=url_pk)
        		this_url.website_img.delete()
        		this_url.delete()
			return Response(status=status.HTTP_204_NO_CONTENT)
        	if request.method == 'GET':
                	serializer = URLSerializer(url)
                	return Response(serializer.data)
        except URL.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

class URLList(generics.ListCreateAPIView):
	queryset = URL.objects.all()
	serializer_class = URLDetailSerializer

class URLCreateUpdateAPIView(CreateAPIView):
	queryset = URL.objects.all()
	serializer_class = URLCreateUpdateSerializer
class URLDetail(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = URLDetailSerializer
	queryset = URL.objects.all()
