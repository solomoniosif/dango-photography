from django import forms
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, Row, Column, HTML, ButtonHolder, Submit
from .custom_layout_object import Formset

from .models import Post
from photos.models import Photo, Album


class PostForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(PostForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = True
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-md-3 create-label'
		self.helper.field_class = 'col-md-9 mb-1'
		self.helper.layout = Layout(
			Div(
				Field('title', placeholder="Title"),
				Field('status'),
				Field('text'),
				Field('tags'),
				Field('slug'),
				HTML("<hr>"),
				Fieldset('Add photos to post', Formset('post_photos')),
				HTML("<br>"),
				ButtonHolder(Submit('submit', 'Create Post')),
			)
		)

	class Meta:
		model = Post
		fields = ['title', 'status', 'text', 'tags', 'slug']


class PostForm2(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title', 'status', 'text', 'tags', 'slug']


class PostForm3(forms.ModelForm):
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
