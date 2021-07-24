from django.urls import path
from . import views

urlpatterns = [
	path('post/<slug:slug>', views.PostDetailView.as_view(), name='post_detail'),
]
