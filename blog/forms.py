from django import forms

from .models import Post
from photos.models import Photo, Album


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title', 'status', 'text', 'tags']
		widgets = {
			'title': forms.TextInput(attrs={
			}),
			'status': forms.Select(),
			'text': forms.Textarea(attrs={
				'placeholder': 'Add post text here',
				'rows': 7,
				'cols': 70
			}),
		}


class PhotoForm(forms.ModelForm):
	class Meta:
		model = Photo
		fields = ['image', 'description', 'is_featured']
		widgets = {
			'image': forms.FileInput(attrs={
				'style': 'width: 240px;'
			}),
			'description': forms.Textarea(attrs={
				'placeholder': 'Add a short photo description that will be displayed below the photo (optional)',
				'rows': 1,
				'cols': 70
			}),
		}


class SelectAlbumForm(forms.Form):
	album = forms.ModelChoiceField(queryset=Album.objects.all())
