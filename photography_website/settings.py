"""
Django settings for photography_website project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from pathlib import Path
import os
import django_heroku
import dj_database_url
from decouple import config

import cloudinary
import cloudinary.uploader
import cloudinary.api

# from cloudinary_api_secrets import CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9r+6dqh-#+1w9d1=ad)phh3i#l#o-ncq-4gek$wip1=u-z%ws-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['django-photography.herokuapp.com', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.sites',

	# Third party apps
	'taggit',
	'cloudinary',
	"crispy_forms",
	# 'forms_fieldset',
	'extra_views',
	# 'widget_tweaks',
	# 'debug_toolbar',
	'django_comments_xtd',
	'django_comments',

	# Local apps
	'core',
	'accounts',
	'photos',
	'blog',
]

MIDDLEWARE = [
	# 'debug_toolbar.middleware.DebugToolbarMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'photography_website.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [BASE_DIR / 'templates'],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'photography_website.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': BASE_DIR / 'db.sqlite3',
	}
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static', ]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Configuration
AUTH_USER_MODEL = 'accounts.CustomUser'

# Taggit Configuration
TAGGIT_CASE_INSENSITIVE = True

# Django crispy forms Configuration
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')

cloudinary.config(
	cloud_name=CLOUDINARY_CLOUD_NAME,
	api_key=CLOUDINARY_API_KEY,
	api_secret=CLOUDINARY_API_SECRET
)

# Django Comments Xtd Configuration
COMMENTS_APP = 'django_comments_xtd'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#  To help obfuscating comments before they are sent for confirmation.
COMMENTS_XTD_SALT = (b"Timendi causa est nescire. "
					 b"Aequam memento rebus in arduis servare mentem.")

# Source mail address used for notifications.
COMMENTS_XTD_FROM_EMAIL = "noreply@example.com"

# Contact mail address to show in messages.
COMMENTS_XTD_CONTACT_EMAIL = "helpdesk@example.com"

SITE_ID = 1

COMMENTS_XTD_MAX_THREAD_LEVEL = 1  # default is 0
COMMENTS_XTD_LIST_ORDER = ('-thread_id', 'order')  # default is ('thread_id', 'order')

#
# # DEBUG_TOOLBAR_CONFIG
# INTERNAL_IPS = ('127.0.0.1',)
#
# def show_toolbar(request):
# 	return True
#
# DEBUG_TOOLBAR_CONFIG = {
# 	'INTERCEPT_REDIRECTS': False,
# 	"SHOW_TOOLBAR_CALLBACK": show_toolbar,
# 	'INSERT_BEFORE': '</head>'
# }
#
# DEBUG_TOOLBAR_PANELS = [
# 	'debug_toolbar.panels.history.HistoryPanel',
# 	'debug_toolbar.panels.versions.VersionsPanel',
# 	'debug_toolbar.panels.timer.TimerPanel',
# 	'debug_toolbar.panels.settings.SettingsPanel',
# 	'debug_toolbar.panels.headers.HeadersPanel',
# 	'debug_toolbar.panels.request.RequestPanel',
# 	'debug_toolbar.panels.sql.SQLPanel',
# 	'debug_toolbar.panels.staticfiles.StaticFilesPanel',
# 	'debug_toolbar.panels.templates.TemplatesPanel',
# 	'debug_toolbar.panels.cache.CachePanel',
# 	'debug_toolbar.panels.signals.SignalsPanel',
# 	'debug_toolbar.panels.logging.LoggingPanel',
# 	'debug_toolbar.panels.redirects.RedirectsPanel',
# 	'debug_toolbar.panels.profiling.ProfilingPanel',
# ]

# Whitenoise Configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Django Heroku Configurations
django_heroku.settings(locals())
