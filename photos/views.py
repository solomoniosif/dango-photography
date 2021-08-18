from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView, DeleteView
from django.contrib import messages

from .forms import PhotoForm, PhotoFormSet
from .models import Photo, Album


def home(request):
	return render(request, 'photos/index.html')


class PhotoListView(ListView):
	model = Photo
	template_name = 'photos/photo_list.html'
	context_object_name = 'photos'


class PhotoCreateView(TemplateView):
	template_name = 'photos/add_photos.html'

	def get(self, *args, **kwargs):
		formset = PhotoFormSet(queryset=Photo.objects.none())
		return self.render_to_response({'photo_formset': formset})

	def post(self, *args, **kwargs):
		formset = PhotoFormSet(data=self.request.POST)
		if formset.is_valid():
			formset.save()
			return redirect(reverse_lazy('photo_list'))
		return self.render_to_response({'photo_formset': formset})


def upload_photo(request):
	context = dict(backend_form=PhotoForm())

	if request.method == 'POST':
		form = PhotoForm(request.POST, request.FILES)
		context['posted'] = form.instance
		if form.is_valid():
			form.save()

	return render(request, 'photos/add_photo.html', context)


class AlbumListView(ListView):
	model = Album
	template_name = 'photos/album_list.html'
	context_object_name = 'albums'


class AlbumDetailView(DetailView):
	model = Album
	template_name = 'photos/album_detail.html'
	context_object_name = 'album'


class AlbumDeleteView(DeleteView):
	model = Album
	success_url = reverse_lazy('photos:albums')
