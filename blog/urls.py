from django.urls import path
from . import views


urlpatterns = [
	path('', views.PostListView.as_view(), name='blog'),
	path('<slug:slug>', views.PostDetailView.as_view(), name='post_detail'),
	path('create-bulk/', views.PostCreateView.as_view(), name='create_bulk'),
	path('create/', views.PostCreateWithInlinesView.as_view(), name='create'),
	path('create-post/', views.create_post, name='create_post'),
	path('update/<slug:slug>', views.PostUpdateWithInlinesView.as_view(), name='update'),
	path('delete/<slug:slug>', views.PostDeleteView.as_view(), name='delete'),
]
