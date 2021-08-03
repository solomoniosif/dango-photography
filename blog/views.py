from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic.detail import SingleObjectMixin
from django.db import transaction

from .forms import PostForm, PostFormSet
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
	success_url = None

	def get_context_data(self, **kwargs):
		context = super(PostUpdateView, self).get_context_data(**kwargs)
		if self.request.POST:
			context['post_photos'] = PostFormSet(self.request.POST, self.request.FILES, instance=self.object)
		else:
			context['post_photos'] = PostFormSet(instance=self.object)
		return context

	def form_valid(self, form):
		context = self.get_context_data()
		post_photos = context['post_photos']
		with transaction.atomic():
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
