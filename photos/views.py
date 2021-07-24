from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView

from .forms import PhotoFormSet
from .models import Photo


def home(request):
	return render(request, 'photos/index.html')


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


class PhotoListView(ListView):
	model = Photo
	template_name = 'photos/photo_list.html'
	context_object_name = 'photos'
