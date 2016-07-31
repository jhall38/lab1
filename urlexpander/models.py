from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.

class URL(models.Model):
	expanded_url = models.CharField(max_length=500)
	shortend_url = models.CharField(max_length=500)
	status = models.IntegerField()
	page_title = models.CharField(max_length=50)
	
	def get_absolute_url(self):
		return reverse('urlexpander:detail)', kwargs={'pk': self.pk})
