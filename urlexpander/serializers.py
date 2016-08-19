from django.forms import widgets
from rest_framework import serializers
from .models import URL, Archived

class ArchivedSerializer(serializers.ModelSerializer):
	class Meta:
		model = Archived
		fields = ('archived_url', 'timestamp')
class URLDetailSerializer(serializers.ModelSerializer):
	archived = ArchivedSerializer(read_only=True)
	class Meta:
		model = URL
		fields = ('id', 'expanded_url', 'shortend_url', 'status', 'page_title', 'archived', 'website_img')
class URLCreateUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = URL
		fields = ('expanded_url', 'shortend_url', 'status', 'page_title', 'archived', 'website_img')
		read_only_fields = ('expanded_url', 'status', 'page_title', 'archived', 'website_img') 
