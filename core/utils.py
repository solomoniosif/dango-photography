from django.utils.text import slugify


def slugify_pre_save(sender, instance, *args, **kwargs):
	if instance.slug is None or instance.slug == "":
		new_slug = slugify(instance.title)
		instance_class = instance.__class__
		qs = instance_class.objects.filter(
			slug=new_slug).exclude(id=instance.id)
		if qs.count() == 0:
			instance.slug = new_slug
		else:
			instance.slug = f"{new_slug}-{qs.count()}"
