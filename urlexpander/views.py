from django.shortcuts import render, get_object_or_404
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from .models import URL

def index(request):
	all_urls = URL.objects.all()
	return render(request, 'urlexpander/index.html', {'all_urls' : all_urls})

def detail(request, url_pk):
	this_url = get_object_or_404(URL, pk=url_pk)
	return render(request, 'urlexpander/detail.html', {'this_url' : this_url})

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
	except requests.exceptions.RequestException as e: 
		return render(request, 'urlexpander/error.html', {'e' : e})
	return render(request, 'urlexpander/detail.html', {'this_url' : new_url})

def delete(request, url_pk):
	this_url = get_object_or_404(URL, pk=url_pk)
	this_url.delete()
	return render(request, 'urlexpander/index.html', {'all_urls' : URL.objects.all()})
