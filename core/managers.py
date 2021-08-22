from django.db import models
from django.utils import timezone


class PublishedManager(models.Manager):

	def published(self, **kwargs):
		return self.filter(status='PU', **kwargs)
