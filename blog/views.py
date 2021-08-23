from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, CreateView, DeleteView
from django.contrib import messages
from extra_views import InlineFormSetFactory, CreateWithInlinesView, UpdateWithInlinesView, SuccessMessageMixin

from photos.models import Photo, Album
from .forms import PostForm, PhotoForm
from .models import Post


class PostDetailView(DetailView):
	template_name = 'blog/post_details.html'
	model = Post
	context_object_name = 'post'


class PostListView(ListView):
	template_name = 'blog/post_list.html'
	model = Post
	queryset = Post.objects.published()
	context_object_name = 'posts'


class UserPostListView(ListView):
	template_name = 'blog/post_list.html'
	model = Post
	context_object_name = 'posts'

	def get_queryset(self):
		qs = super().get_queryset()
		user_posts = qs.filter(author=self.request.user)
		return user_posts


class PostDeleteView(DeleteView):
	model = Post
	success_url = reverse_lazy('blog:home')


class PostCreateView(CreateView):
	model = Post
	template_name = 'blog/post_create_bulk.html'
	form_class = PostForm
	success_url = None

	def form_valid(self, form):
		form.instance.author = self.request.user
		self.object = form.save()
		photos = self.request.FILES.getlist('photos')
		if photos:
			new_album = Album.objects.create(title=self.object.title) if 'new_album' in self.request.POST else None
			for photo in photos:
				new_photo = Photo.objects.create(
					album=new_album,
					post=self.object,
					tags=self.object.tags,
					image=photo
				)
		messages.success(self.request, f"<b>{self.object.title}</b> created successfully")
		return HttpResponseRedirect(self.get_success_url())

	def get_success_url(self):
		return reverse_lazy('blog:post_detail', kwargs={'slug': self.object.slug})


class PhotoInline(InlineFormSetFactory):
	model = Photo
	form_class = PhotoForm
	fields = ['image', 'description', 'is_featured']
	extra_forms = 1
	can_delete = True

	def get_factory_kwargs(self):
		factory_kwargs = super().get_factory_kwargs()
		factory_kwargs.update({'extra': self.extra_forms})
		return factory_kwargs


class PostCreateWithInlinesView(CreateWithInlinesView):
	model = Post
	form_class = PostForm
	inlines = [PhotoInline, ]
	template_name = 'blog/post_create.html'
	success_url = None

	def forms_valid(self, form, inlines):
		form.instance.author = self.request.user
		self.object = form.save()
		response = self.form_valid(form)
		new_album = Album.objects.create(title=self.object.title) if 'new_album' in self.request.POST else None
		for formset in inlines:
			for form in formset:
				new_photo = form.save(commit=False)
				new_photo.album = new_album
				new_photo.save()
		messages.success(self.request, f"<b>{self.object.title}</b> created successfully")
		return response

	def get_success_url(self):
		return reverse_lazy('blog:post_detail', kwargs={'slug': self.object.slug})


class PostUpdateWithInlinesView(SuccessMessageMixin, UpdateWithInlinesView):
	model = Post
	form_class = PostForm
	inlines = [PhotoInline, ]
	template_name = 'blog/post_update.html'
	success_message = "<b>%(title)s</b> was updated successfully"


@login_required
def add_tags_to_post(request, slug):
	post = get_object_or_404(Post, slug=slug)
	new_tags = request.POST.get('new_tags')
	tag_list = [raw_tag.strip() for raw_tag in new_tags.split(',')]
	for tag in tag_list:
		post.tags.add(tag)
	if len(tag_list) == 1:
		messages.success(request, f"The tag <b>{tag_list[0]}</b> was added to post <b>{post.title}</b>")
	elif len(tag_list) > 1:
		messages.success(request, f"The tags <b>{', '.join(tag_list)}</b> were added to post <b>{post.title}</b>")
	return redirect('blog:post_detail', slug=post.slug)


def search_posts_by_tag(request, tag):
	posts = Post.objects.published().filter(tags__name=tag)
	context = {'tag': tag, 'posts': posts}
	if posts.exists():
		messages.info(request, f"Posts tagged with <b>{tag}</b>")
	else:
		messages.warning(request, f"There are no posts tagged with <b>{tag}</b>")
	return render(request, 'blog/post_list.html', context)
