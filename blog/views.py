from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic.detail import SingleObjectMixin

from .forms import PostForm, PostFormSet, PostInlineFormset
from .models import Post


class PostDetailView(DetailView):
	template_name = 'blog/post_details.html'
	model = Post
	context_object_name = 'post'


class PostListView(ListView):
	template_name = 'blog/post_list.html'
	model = Post
	context_object_name = 'posts'


class PostCreateView(LoginRequiredMixin, CreateView):
	template_name = 'blog/post_form.html'
	success_url = reverse_lazy('blog')
	form_class = PostForm

	def get_context_data(self, **kwargs):
		context = super(PostCreateView, self).get_context_data(**kwargs)
		if self.request.POST:
			context['new_post'] = PostFormSet(self.request.POST)
		else:
			context['new_post'] = PostFormSet()
		return context

	def form_valid(self, form):
		messages.add_message(self.request, messages.SUCCESS, 'The post was created')
		return super().form_valid(form)


class PostInlineEditView(SingleObjectMixin, FormView):
	model = Post
	template_name = 'blog/post_inline_edit.html'

	def get(self, request, *args, **kwargs):
		self.object = self.get_object(queryset=Post.objects.all())
		return super().get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object(queryset=Post.objects.all())
		return super().get(request, *args, **kwargs)

	def get_form(self, form_class=None):
		return PostInlineFormset(**self.get_form_kwargs(), instance=self.object)

	def form_valid(self, form):
		form.save()
		messages.add_message(self.request, messages.SUCCESS, 'Changes were saved.')
		return HttpResponseRedirect(self.get_success_url())

	def get_context_data(self, **kwargs):
		"""Insert the Post Model Form into the context dict."""
		if 'post_form' not in kwargs:
			kwargs['post_form'] = PostForm()
		return super().get_context_data(**kwargs)

	def get_success_url(self):
		return reverse('post_detail', kwargs={'slug': self.object.slug})
