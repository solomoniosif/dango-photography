from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('photos/', views.PhotoListView.as_view(), name='photo_list'),
	path('photos/add/', views.PhotoCreateView.as_view(), name='add_photos'),
	path('photos/add-photo/', views.upload_photo, name='add_photo'),
	path('albums/', views.AlbumListView.as_view(), name='albums'),
	path('albums/<slug:slug>', views.AlbumDetailView.as_view(), name='album_detail'),
]
