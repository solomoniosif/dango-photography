from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
	path('', views.PostListView.as_view(), name='home'),
	path('<slug:slug>', views.PostDetailView.as_view(), name='post_detail'),
	path('create-bulk/', views.PostCreateView.as_view(), name='create_bulk'),
	path('create/', views.PostCreateWithInlinesView.as_view(), name='create'),
	path('update/<slug:slug>', views.PostUpdateWithInlinesView.as_view(), name='update'),
	path('delete/<slug:slug>', views.PostDeleteView.as_view(), name='delete'),
]
