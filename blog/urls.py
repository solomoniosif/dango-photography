from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
	path('', views.PostListView.as_view(), name='home'),
	path('user/<str:username>/', views.UserPostListView.as_view(), name='user_posts'),
	path('<slug:slug>', views.PostDetailView.as_view(), name='post_detail'),
	path('create/', views.PostCreateWithInlinesView.as_view(), name='create'),
	path('create-bulk/', views.PostCreateView.as_view(), name='create_bulk'),
	path('update/<slug:slug>', views.PostUpdateWithInlinesView.as_view(), name='update'),
	path('delete/<slug:slug>', views.PostDeleteView.as_view(), name='delete'),
	path('<slug:slug>/add-tags/', views.add_tags_to_post, name='add_tags'),
	path('tag/<str:tag>', views.search_posts_by_tag, name='search_by_tag'),
]
