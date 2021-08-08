from django.urls import path
from . import views

urlpatterns = [
	path('', views.PostListView.as_view(), name='blog'),
	path('<slug:slug>', views.PostDetailView.as_view(), name='post_detail'),
	path('add/', views.PostCreateView.as_view(), name='post_create'),
	path('update/<slug:slug>', views.PostUpdateView.as_view(), name='post_update'),
	path('create-post/', views.create_post, name='create_post'),
	path('update-post/<slug:slug>', views.EditPostPhotos.as_view(), name='update_post'),
]
