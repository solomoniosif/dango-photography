from django.contrib import admin

from photos.models import Gallery, Album, Photo


class GalleryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}


class PhotoInline(admin.TabularInline):
	model = Photo


class AlbumAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}
	list_display = ('title', 'photos', 'is_featured')
	list_editable = ('is_featured',)
	inlines = [PhotoInline]

	def get_queryset(self, request):
		return super().get_queryset(request).prefetch_related('photos')

	@admin.display(description="Photos")
	def photos(self, obj):
		return obj.photos.all().count()


class PhotoAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}
	list_display = ('title', 'tag_list', 'album', 'is_featured')
	list_editable = ('is_featured',)

	# Get list of tags
	def get_queryset(self, request):
		return super().get_queryset(request).prefetch_related('tags')

	@admin.display(description="Tags")
	def tag_list(self, obj):
		return u", ".join(o.name for o in obj.tags.all())


admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)
