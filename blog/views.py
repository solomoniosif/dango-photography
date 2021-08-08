from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import View, DetailView, ListView, CreateView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic.detail import SingleObjectMixin
from django.db import transaction

from extra_views import InlineFormSetView, UpdateWithInlinesView, InlineFormSetFactory

from photos.models import Photo, Album
from .forms import PostForm, PostForm2, PostFormSet, PhotoForm
from .models import Post


class PostDetailView(DetailView):
	template_name = 'blog/post_details.html'
	model = Post
	context_object_name = 'post'


class PostListView(ListView):
	template_name = 'blog/post_list.html'
	model = Post
	context_object_name = 'posts'


class PostCreateView(CreateView):
	model = Post
	template_name = 'blog/post_create.html'
	form_class = PostForm
	success_url = None

	def get_context_data(self, **kwargs):
		context = super(PostCreateView, self).get_context_data(**kwargs)
		if self.request.POST:
			context['post_photos'] = PostFormSet(self.request.POST, self.request.FILES)
		else:
			context['post_photos'] = PostFormSet()
		return context

	def form_valid(self, form):
		context = self.get_context_data()
		post_photos = context['post_photos']
		with transaction.atomic():
			if post_photos.is_valid():
				self.object = form.save()
				post_photos.instance = self.object
				post_photos.save()
				messages.add_message(self.request, messages.SUCCESS, f"Post '{self.object.title}' was created.")
				return super(PostCreateView, self).form_valid(form)
			else:
				return render(self.request, self.template_name, self.get_context_data(form=form))

	def get_success_url(self):
		return reverse_lazy('post_detail', kwargs={'slug': self.object.slug})


class PostUpdateView(UpdateView):
	model = Post
	template_name = 'blog/post_update.html'
	form_class = PostForm
	formset_class = PostFormSet
	success_url = None

	def get_context_data(self, **kwargs):
		context = super(PostUpdateView, self).get_context_data(**kwargs)
		if self.request.POST:
			context['post_photos'] = PostFormSet(self.request.POST, self.request.FILES, instance=self.object)
		else:
			context['post_photos'] = PostFormSet(instance=self.object)
		return context

	# def post(self, request, *args, **kwargs):
	# 	self.object = self.get_object()
	# 	form_class = self.get_form_class()
	# 	form = self.get_form(form_class)
	# 	formset = PostFormSet(self.request.POST, self.request.FILES, instance=self.object)
	#
	# 	if form.is_valid():
	# 		for fs in formset:
	# 			if fs.is_valid():
	# 				fs.save()
	# 		messages.success(self.request, 'Post edited successfully')
	# 		return self.form_valid(form)
	# 	return self.form_invalid(form)

	def form_valid(self, form):
		context = self.get_context_data()
		post_photos = context['post_photos']
		if post_photos.is_valid():
			self.object = form.save()
			post_photos.instance = self.object
			post_photos.save()
			messages.add_message(self.request, messages.SUCCESS, f"Post '{self.object.title}' was updated.")
			return super(PostUpdateView, self).form_valid(form)
		else:
			return render(self.request, self.template_name, self.get_context_data(form=form))

	def get_success_url(self):
		return reverse_lazy('post_detail', kwargs={'slug': self.object.slug})


############################################################
############################################################

class PhotoInline(InlineFormSetFactory):
	model = Photo
	form_class = PhotoForm
	fields = ['image', 'description', 'is_featured']



	def get_factory_kwargs(self):
		factory_kwargs = super().get_factory_kwargs()
		factory_kwargs.update({'extra': 1})
		print(factory_kwargs)
		return factory_kwargs


class EditPostPhotos(UpdateWithInlinesView):
	model = Post
	form_class = PostForm2
	inlines = [PhotoInline, ]
	template_name = 'blog/post_and_photos.html'
	# fields = ['title', 'status', 'text', 'tags']
	factory_kwargs = {'extra': 1}


############################################################
############################################################


def create_post(request):
	if request.method == 'POST':
		post_data = request.POST
		photos = request.FILES.getlist('photos')

		new_post = Post.objects.create(
			author=request.user,
			title=post_data['title'],
			status=post_data['status'],
			text=post_data['text'],
			tags=post_data['tags']
		)
		if photos:
			new_album = Album.objects.create(title=post_data['title'])
			for photo in photos:
				new_photo = Photo.objects.create(
					album=new_album,
					post=new_post,
					tags=post_data['tags'],
					image=photo,
				)
		messages.success(request, f"'{post_data['title']}' created successfully")
		return reverse_lazy('post_detail', kwargs={'slug': new_post.slug})

	return render(request, 'blog/post_form.html')
