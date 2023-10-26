from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-o6#p5o^9h_i#js@zhxke456v7six337(%0$l#k&l*!!62!u9sz'


DEBUG = True


ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local applications
    'Inventory',
    'Demo',
    'DRF',
    'Search',
    'Promotion',
    'Cart',
    'Account',
    'Payment',
    'Orders',
    'Delivery',

    # third-party packages
    'mptt',
    'django_countries',
    'django_elasticsearch_dsl',
    'rest_framework',

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


ROOT_URLCONF = 'Acorn.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "templates"
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'Cart.context_processors.cart',
            ],
        },
    },
]


WSGI_APPLICATION = 'Acorn.wsgi.application'


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'PapaKarlo1',
        'PASSWORD': 'tem_123123123',
        'HOST': '127.0.0.1',
        # 'HOST': 'pgdb',
        'PORT': '5432',
    }
}


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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False


STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


INTERNAL_IPS = [
    "127.0.0.1",
]


ELASTICSEARCH_DSL = {
    "default": {"hosts": "localhost:9200"}
}

# ELASTICSEARCH_DSL = {
#     "default": {"hosts": "elasticsearch"}
# }


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}


CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"

BASKET_SESSION_ID = "Cart items"

# Custom user model
AUTH_USER_MODEL = 'Account.UserModel'
LOGIN_REDIRECT_URL = '/account/dashboard'
LOGIN_URL = '/account/login'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Stripe payment
PUBLISHABLE_KEY = "pk_test_51O3IqsKByHITeWBfhCYeW5TCpt11K2toSynUIEEITxxVv7UK0vaayIGDKU3LlbR2ckM20mA1263E766P9b2kA8Wy00iRRGZ3Q1"
SECRET_KEY = "sk_test_51O3IqsKByHITeWBfGGlzr3oFq3RXiyzAv9m4b5W1wlmmGzJVZckxND1bxJIFpUpcV8ZLgKyqztW1wN8PLf4f2rDV00AJKpneQt"
STRIPE_ENDPOINT_SECRET = 'whsec_137efa2f56ea7d130c000c5140d86475e58562db366aa8be59db2b9520b62aa0'
# ..\stripe listen --forward-to localhost:8000/payment/webhook/