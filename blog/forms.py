from django import forms
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import Formset

from .models import Post
from photos.models import Photo


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
				Field('author'),
				Field('status'),
				Field('text'),
				Field('tags'),
				Field('slug'),
				HTML("<hr>"),
				Fieldset('Add photos', Formset('post_photos')),
				HTML("<br>"),
				ButtonHolder(Submit('submit', 'Create Post')),
			)
		)

	class Meta:
		model = Post
		fields = ['title', 'author', 'status', 'text', 'tags', 'slug']


class PostForm2(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(PostForm2, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = True
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'floatingInput'
		self.helper.field_class = 'col-md-9'
		self.helper.layout = Layout(
			Div(
				Field('title'),
				Field('author'),
				Field('status'),
				Field('text', css_class="form-floating"),
				Field('tags'),
				Field('slug'),
				HTML("<br>"),
				ButtonHolder(Submit('submit', 'Create Post')),
			)
		)

	class Meta:
		model = Post
		fields = ['title', 'author', 'status', 'text', 'tags', 'slug']


class PhotoForm(forms.ModelForm):
	class Meta:
		model = Photo
		fields = ['image', 'description', 'is_featured']
		widgets = {
			'image': forms.FileInput(attrs={
				'style': 'width: 240px;'
			}),
			'description': forms.Textarea(attrs={
				'placeholder': 'Add a short photo description that will be displayed below the photo on the post (optional)',
				'rows': 1,
				'cols': 70
			}),
		}


PostFormSet = inlineformset_factory(Post, Photo, form=PhotoForm, extra=2, can_delete=True)
