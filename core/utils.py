from django.utils.text import slugify
from string import ascii_lowercase
import random


def slugify_pre_save(sender, instance, *args, **kwargs):
	if instance.slug is None or instance.slug == "":
		new_slug = slugify(instance.title)
		instance_class = instance.__class__
		qs = instance_class.objects.filter(
			slug=new_slug).exclude(id=instance.id)
		if qs.count() == 0:
			instance.slug = new_slug
		else:
			random_string = ''.join([random.choice(ascii_lowercase) for _ in range(9)])
			instance.slug = f"{new_slug}-{random_string}"
