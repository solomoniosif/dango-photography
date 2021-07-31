from django.urls import path
from . import views

urlpatterns = [
	path('', views.PostListView.as_view(), name='blog'),
	path('<slug:slug>', views.PostDetailView.as_view(), name='post_detail'),
	path('add/', views.PostCreateView.as_view(), name='add_post'),
	path('update/<slug:slug>', views.PostInlineEditView.as_view(), name='post_inline_update'),
]
