from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Post


class PostDetailView(DetailView):
	template_name = 'blog/post_details.html'
	model = Post
	context_object_name = 'post'


class PostListView(ListView):
	template_name = 'blog/post_list.html'
	model = Post
	context_object_name = 'posts'

