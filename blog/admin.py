from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
	fields = ('status', 'author', 'title', 'text', 'photos', 'album', 'tags', 'slug')
	list_display = ('title', 'slug', 'status', 'created_on')
	list_filter = ("status",)
	search_fields = ['title', 'text']
	prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin)
