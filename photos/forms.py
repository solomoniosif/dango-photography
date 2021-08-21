from django import forms
from .models import Photo, Album


class PhotoForm(forms.ModelForm):
	class Meta:
		model = Photo
		fields = '__all__'


PhotoFormSet = forms.modelformset_factory(
	Photo, fields=('title', 'album', 'tags', 'image', 'is_featured'), extra=1
)


class AlbumForm(forms.ModelForm):
	class Meta:
		model = Album
		fields = ['title', 'is_featured']
