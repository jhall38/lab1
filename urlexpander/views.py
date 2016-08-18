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
from .models import URL, Archived

@login_required(login_url='/login/')
def index(request):
	all_urls = URL.objects.all()
	return render(request, 'urlexpander/index.html', {'all_urls' : all_urls})

@login_required(login_url='/login/')
def detail(request, url_pk):
	this_url = get_object_or_404(URL, pk=url_pk)
	try:
		this_archive = Archived.objects.get(url=this_url)
		return render(request, 'urlexpander/detail.html', {'this_url' : this_url, 'this_archive' : this_archive})
	except:
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
			new_archived.url = new_url
			new_archived.save()
			
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

def delete(request, url_pk):
	this_url = get_object_or_404(URL, pk=url_pk)
	this_url.delete()
	return render(request, 'urlexpander/index.html', {'all_urls' : URL.objects.all()})
