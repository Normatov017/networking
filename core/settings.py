import os
from pathlib import Path
import dj_database_url # Ma'lumotlar bazasi URL'ni tahlil qilish uchun

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Productionda SECRET_KEY ni environment variable dan olamiz
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-zpaw7w=55ho1#z!t^bvu3+4_#op2h)ghmyf_x++&4yc3e+*8^t')

# SECURITY WARNING: don't run with debug turned on in production!
# Productionda DEBUG ni False ga o'zgartiramiz. Environment variable orqali boshqarish tavsiya etiladi.
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

# Productionda serveringizning IP manzillari yoki domen nomlari
ALLOWED_HOSTS = ['*']
# Agar siz hostni o'rnatmoqchi bo'lmasangiz, shunday qilib qo'yishingiz mumkin:
# ALLOWED_HOSTS = ['*'] # Qat'iy tavsiya etilmaydi! Faqat test uchun.


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'products',
    'customers',
    'orders',
    'warehouses',
    'crispy_forms',
    'crispy_bootstrap5',
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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'core' / 'templates'],
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
WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Ma'lumotlar bazasi sozlamalari. Environment variable orqali boshqarish
# Bulut muhitida DATABASE_URL ko'pincha avtomatik ravishda o'rnatiladi (masalan, Heroku, Render)
# Yoki o'zingiz belgilashingiz mumkin (masalan, 'postgres://user:password@host:port/dbname')

    # Mahalliy rivojlanish uchun standart sozlamalar

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "Networking",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tashkent' # O'zbekiston uchun vaqt zonasi
# USE_I18N = True # Default True
# USE_L10N = True # Django 4.0 dan o'chirilgan, USE_TZ bilan birga ishlaydi
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' # Joylashtirish uchun

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


JAZZMIN_SETTINGS = {
    "site_title": "Ulgurji ERP/CRM/WMS",
    "site_header": "Ulgurji Savdo",
    "site_brand": "Kompaniya Paneli",
    "site_logo": "img/logo.png", # O'zingizning logotipingizga yo'l
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": "Xush kelibsiz, Ulgurji Savdo tizimiga xush kelibsiz!",
    "copyright": "Ulgurji Kompaniyasi",
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Bosh sahifa", "url": "home", "permissions": ["auth.view_user"]},
        {"name": "Statistika", "url": "dashboard", "permissions": ["auth.view_user"]}, # 'dashboard' nomli URLga ishora qiladi
        {"model": "auth.User"},
        {"app": "products"},
        {"app": "customers"},
        {"app": "orders"},
        {"app": "warehouses"},
    ],
    "usermenu_links": [
        {"name": "Veb-sayt", "url": "home"}, # Keyinchalik yaratamiz
        {"model": "auth.User"}
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["products", "customers", "orders", "warehouses", "auth"],
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"auth.user": "vertical_tabs", "auth.group": "vertical_tabs"},
    "small_sidemenu": False,
    "separate_apps": True,
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "products.Product": "fas fa-box",
        "customers.Customer": "fas fa-user-tie",
        "orders.Order": "fas fa-shopping-cart",
        "warehouses.Warehouse": "fas fa-warehouse",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
}