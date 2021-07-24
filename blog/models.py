from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save

from photography_website import settings
from core.models import BasePublishModel
from core.utils import slugify_pre_save
from photos.models import Photo


class Post(BasePublishModel):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
	title = models.CharField(max_length=255)
	text = RichTextField(null=True, blank=True)
	slug = models.SlugField(null=True, blank=True, db_index=True)
	photos = models.ManyToManyField(Photo)

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-updated_on', '-created_on']
		verbose_name = 'Post'
		verbose_name_plural = 'Posts'


pre_save.connect(slugify_pre_save, sender=Post)
