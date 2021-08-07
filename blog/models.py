from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from taggit.managers import TaggableManager

from photography_website import settings
from core.models import BasePublishModel
from core.utils import slugify_pre_save


class Post(BasePublishModel):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
	title = models.CharField(max_length=255)
	text = models.TextField(null=True, blank=True)
	slug = models.SlugField(null=True, blank=True, db_index=True)
	tags = TaggableManager()

	def get_featured_image_url(self):
		images = self.post_photos.all()
		if images.exists():
			try:
				featured_image = images.filter(is_featured=True).first()
				return featured_image.image.url
			except:
				featured_image = images.first()
				return featured_image.image.url
		else:
			return ''

	def get_absolute_url(self):
		return reverse('post_detail', args=[self.slug])

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-updated_on', '-created_on']
		verbose_name = 'Post'
		verbose_name_plural = 'Posts'


pre_save.connect(slugify_pre_save, sender=Post)
