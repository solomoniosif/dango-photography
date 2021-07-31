from django import forms
from django.forms.models import inlineformset_factory

from .models import Post
from photos.models import Photo


class PostForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(PostForm, self).__init__(*args, **kwargs)

	class Meta:
		model = Post
		fields = ['title', 'author', 'status', 'text', 'tags', 'slug']


class PhotoForm(forms.ModelForm):
	class Meta:
		model = Photo
		fields = ['image', 'title', 'tags', 'description', 'is_featured']
		widgets = {
			'image': forms.FileInput(attrs={
				'style': 'width: 180px;'
			}),
			'title': forms.TextInput(attrs={
				'placeholder': 'Enter title (optional)',
				'style': 'width: 300px;'
			}),
			'tags': forms.TextInput(attrs={
				'placeholder': 'A comma-separated list of tags (optional)',
				'style': 'width: 300px;'
			}),
			'description': forms.Textarea(attrs={
				'placeholder': 'Add a short photo description that will be displayed below the photo on the post (optional)',
				'rows': 2,
				'cols': 50
			}),
		}


PostFormSet = inlineformset_factory(Post, Photo, form=PhotoForm)

PostInlineFormset = inlineformset_factory(Post, Photo, fields=('image', 'title', 'tags', 'description', 'is_featured'),
										  extra=1)
