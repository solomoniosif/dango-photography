from django.db import models
from django.db.models.signals import pre_save

from taggit.managers import TaggableManager
from cloudinary.models import CloudinaryField

from blog.models import Post
from core.utils import slugify_pre_save


class Gallery(models.Model):
	title = models.CharField(max_length=200, null=False, blank=False)
	slug = models.SlugField(null=True, blank=True, db_index=True)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Gallery'
		verbose_name_plural = 'Galleries'


class Album(models.Model):
	title = models.CharField(max_length=200, null=False, blank=False)
	gallery = models.ForeignKey(Gallery, on_delete=models.SET_NULL, null=True, blank=True)
	slug = models.SlugField(null=True, blank=True, db_index=True)
	is_featured = models.BooleanField(default=False)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Album'
		verbose_name_plural = 'Albums'


class Photo(models.Model):
	album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name="photos")
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_photos", null=True, blank=True)
	title = models.CharField(max_length=250, null=True, blank=True)
	tags = TaggableManager(blank=True, help_text=None)
	image = CloudinaryField("Image", overwrite=True, resource_type="image", transformation={"quality": "auto:eco"})
	alt = models.CharField(max_length=60, default="error.jpg")
	description = models.TextField(null=True, blank=True)
	slug = models.SlugField(null=True, blank=True, unique=True, db_index=True)
	is_featured = models.BooleanField(default=False)

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.title:
			self.title = self.image.name
		super(Photo, self).save(*args, **kwargs)

	class Meta:
		verbose_name = "photo"
		verbose_name_plural = "photos"


pre_save.connect(slugify_pre_save, sender=Photo)
