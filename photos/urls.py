from django.urls import path
from . import views

app_name = 'photos'

urlpatterns = [
	path('', views.home, name='home'),
	path('photos/', views.PhotoListView.as_view(), name='photo_list'),
	path('photos/add/', views.PhotoCreateView.as_view(), name='add_photos'),
	path('photos/add-photo/', views.upload_photo, name='add_photo'),
	path('albums/', views.AlbumListView.as_view(), name='albums'),
	path('albums/<slug:slug>', views.AlbumDetailView.as_view(), name='album_detail'),
	path('albums/delete/<slug:slug>', views.AlbumDeleteView.as_view(), name='album_delete'),
	path('search/', views.SearchView.as_view(), name='search'),
	path('private-gallery/<str:token>/', views.private_gallery_view, name='private_gallery')
]
