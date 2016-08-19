from django.db import models
from django.core.urlresolvers import reverse
from django.core.files.storage import default_storage
# Create your models here.


class Archived(models.Model):
	archived_url = models.CharField(max_length=500)
	timestamp = models.DateTimeField()

class URL(models.Model):
	expanded_url = models.CharField(max_length=500)
	shortend_url = models.CharField(max_length=500)
	status = models.IntegerField()
	page_title = models.CharField(max_length=50)
	website_img = models.ImageField(upload_to='images', default='image_not_available.jpg')
	archived = models.OneToOneField(Archived, null=True)
	def get_absolute_url(self):
		return reverse('urlexpander:detail)', kwargs={'pk': self.pk})

