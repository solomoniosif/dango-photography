from django.db import models
from django.utils import timezone


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
		if self.state_is_published and self.published_on is None:
			self.published_on = timezone.now()
		else:
			self.published_on = None
		super().save(*args, **kwargs)

	@property
	def state_is_published(self):
		return self.status == self.PublishStatus.PUBLISHED

	@property
	def is_published(self):
		return self.state_is_published and self.published_on < timezone.now()

	class Meta:
		abstract = True
