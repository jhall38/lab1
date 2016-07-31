from django.shortcuts import render, get_object_or_404
from urllib.request import urlopen
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
	html = urlopen(shortend_url)
	soup = BeautifulSoup(html)
	new_url = URL()
	new_url.shortend_url = shortend_url
	new_url.expanded_url = html.geturl()
	new_url.status = html.getcode()
	new_url.page_title = soup.html.head.title.contents[0]
	new_url.save()
	return render(request, 'urlexpander/detail.html', {'this_url' : new_url})

def delete(request, url_pk):
	this_url = get_object_or_404(URL, pk=url_pk)
	this_url.delete()
	return render(request, 'urlexpander/index.html', {'all_urls' : URL.objects.all()})
