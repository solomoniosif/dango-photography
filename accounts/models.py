from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class CustomUser(AbstractUser):
	pass

	# add additional fields in here

	def __str__(self):
		return self.username
