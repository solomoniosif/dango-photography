from django.forms import ModelForm, modelformset_factory
from .models import Photo


class PhotoForm(ModelForm):
	class Meta:
		model = Photo
		fields = '__all__'


PhotoFormSet = modelformset_factory(
	Photo, fields=('title', 'album', 'tags', 'image', 'is_featured'), extra=1
)
