from django.db import models
from django.utils import timezone

from .managers import PublishedManager


class BasePublishModel(models.Model):
	class PublishStatus(models.TextChoices):
		DRAFT = 'DR', 'Draft'
		PUBLISHED = 'PU', 'Published'
		PRIVATE = 'PR', 'Private'

	status = models.CharField(max_length=2, default=PublishStatus.DRAFT, choices=PublishStatus.choices)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	published_on = models.DateTimeField(
		auto_now_add=False, auto_now=False, null=True)

	def save(self, *args, **kwargs):
		if self.is_published and self.published_on is None:
			self.published_on = timezone.now()
		else:
			self.published_on = None
		super().save(*args, **kwargs)

	@property
	def is_published(self):
		return self.status == self.PublishStatus.PUBLISHED

	@property
	def is_draft(self):
		return self.status == self.PublishStatus.DRAFT

	@property
	def is_private(self):
		return self.status == self.PublishStatus.PRIVATE

	objects = PublishedManager()

	class Meta:
		abstract = True
