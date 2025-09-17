import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'gerenciamento_home',
    'gerenciamento_vender',
    'gerenciamento_inteligencia_mercado',
    'gerenciamento_aprenda',
    'gerenciamento_acordos',
    'gerenciamento_oportunidades',
    'gerenciamento_destino',
    'gerenciamento_noticias',
    'gerenciamento_artigos',
    'taggit',
    'tinymce',
    'django_recaptcha',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'configuracoes_projeto.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'frontend'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'gerenciamento_home.context_processors.global_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'configuracoes_projeto.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', cast=int),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Boa_Vista'

USE_I18N = True

USE_L10N = False

USE_TZ = True

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'frontend',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')

AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')

AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')

AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = config('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY')

RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CSRF_COOKIE_SECURE = True

# SESSION_COOKIE_SECURE = True

# SECURE_SSL_REDIRECT = True

# SECURE_HSTS_SECONDS = 31536000

# SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# SECURE_HSTS_PRELOAD = True

TINYMCE_DEFAULT_CONFIG = {
    "height": "320px",
    "width": "960px",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
               "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
               "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
               "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
               "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
               "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
}

TAGGIT_STRIP_UNICODE_WHEN_SLUGIFYING = True

X_FRAME_OPTIONS = 'SAMEORIGIN'

LOGIN_REDIRECT_URL = '/quero-vender/dashboard/' 

LOGIN_URL = '/quero-vender/acessar/'