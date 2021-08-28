from django.db import models
import secrets
from django.utils import timezone
from django.db.models.signals import pre_save
from django.urls import reverse

from taggit.managers import TaggableManager
from cloudinary.models import CloudinaryField

from photography_website import settings
from blog.models import Post
from core.utils import slugify_pre_save


class Album(models.Model):
	title = models.CharField(max_length=200, null=False, blank=False)
	slug = models.SlugField(null=True, blank=True, db_index=True)
	is_featured = models.BooleanField(default=False)
	is_private = models.BooleanField(default=False)

	def __str__(self):
		return self.title

	def get_featured_image_url(self):
		images = self.photos.all()
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
		return reverse('photos:album_detail', args=[self.slug])

	class Meta:
		verbose_name = 'Album'
		verbose_name_plural = 'Albums'
		ordering = ['-is_featured', '-id']


def get_default_token_expiry_date(weeks=26):
	return timezone.localtime(timezone.now()) + timezone.timedelta(weeks=weeks)


class AlbumToken(models.Model):
	album = models.ForeignKey(Album, on_delete=models.CASCADE)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
	token = models.CharField(max_length=255, default=secrets.token_urlsafe(16))
	creation_date = models.DateTimeField(auto_now_add=True)
	expiry_date = models.DateTimeField(default=get_default_token_expiry_date)

	def __str__(self):
		if self.user:
			return f"{self.user.username.title()}'s token for album '{self.album.title}'"
		return f"Anonymous token for album '{self.album.title}'"

	class Meta:
		verbose_name = 'Album Token'
		verbose_name_plural = 'Albums Tokens'


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
		ordering = ['id']


pre_save.connect(slugify_pre_save, sender=Album)
pre_save.connect(slugify_pre_save, sender=Photo)
