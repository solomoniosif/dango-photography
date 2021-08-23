from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView, DeleteView
from django.contrib import messages

from blog.models import Post
from .forms import PhotoForm, PhotoFormSet, AlbumForm
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


class AlbumCreateView(CreateView):
	template_name = "photos/album_create.html"
	success_url = reverse_lazy('products')
	form_class = AlbumForm


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


class SearchView(TemplateView):
	template_name = 'photos/search_results.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		query = self.request.GET.get('q')
		posts = Post.objects.distinct().filter(
			Q(title__icontains=query) | Q(text__icontains=query) | Q(tags__name__icontains=query))
		albums = Album.objects.distinct().filter(Q(title__icontains=query))
		if not posts.exists() and not albums.exists():
			messages.error(self.request, f"No search results for <b>{query}</b>")
		else:
			context['posts'] = posts
			context['albums'] = albums
			messages.info(self.request, f"Search results for <b>{query}</b>")
		return context
