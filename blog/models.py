from django.db.models.signals import pre_save
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import BasePublishModel
from core.utils import slugify_pre_save

from django.db import models
from photos.models import Photo, Album
from photography_website import settings

from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager


class Post(BasePublishModel):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
	title = models.CharField(max_length=255)
	text = RichTextField(null=True, blank=True)
	slug = models.SlugField(null=True, blank=True, db_index=True)
	photos = models.ManyToManyField(Photo)
	album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)
	tags = TaggableManager()

	def save(self):
		pass

	def get_absolute_url(self):
		return reverse('post_detail', args=[self.slug])

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-updated_on', '-created_on']
		verbose_name = 'Post'
		verbose_name_plural = 'Posts'


pre_save.connect(slugify_pre_save, sender=Post)
