from django.shortcuts import render, get_object_or_404
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
	new_url.shortend_url = shortend_url
	new_url.expanded_url = "expanded"
	new_url.status = 69
	new_url.page_title = "title"
	new_url.save()
	return render(request, 'urlexpander/detail.html', {'this_url' : new_url})

def delete(request, url_pk):
	this_url = get_object_or_404(URL, pk=url_pk)
	this_url.delete()
	return render(request, 'urlexpander/index.html', {'all_urls' : URL.objects.all()})
