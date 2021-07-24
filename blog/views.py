from django.shortcuts import render
from django.views.generic import DetailView

from .models import Post


class PostDetailView(DetailView):
	template_name = 'blog/post_details.html'
	model = Post
	context_object_name = 'post'


