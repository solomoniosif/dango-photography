from django.forms import modelformset_factory
from .models import Photo

PhotoFormSet = modelformset_factory(
	Photo, fields=('title', 'categories', 'album', 'tags', 'image', 'is_featured'), extra=1
)
