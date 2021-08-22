"""photography_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar

urlpatterns = [
				  path('admin/', admin.site.urls),
				  # path('__debug__/', include(debug_toolbar.urls)),
				  path('accounts/', include('accounts.urls')),
				  # path('accounts/', include('django.contrib.auth.urls')),
				  path('', include('photos.urls', namespace='photos')),
				  path('blog/', include('blog.urls', namespace='blog')),
				  path(r'comments/', include('django_comments_xtd.urls')),
			  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Django Photography"
admin.site.site_title = "Django Photography"

if settings.DEBUG:
	from django.conf.urls.static import static
	import debug_toolbar
	import mimetypes

	mimetypes.add_type("application/javascript", ".js", True)

	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

	urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns

SHOW_TOOLBAR_CALLBACK = True
