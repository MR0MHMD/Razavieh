from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# 🔑 امنیت پایه
SECRET_KEY = 'django-insecure-8-c*&%_^o%v^@bih9$ob7(p$=t0&8@r$68ma%%@*6ujz#g2m2e'
DEBUG = True
ALLOWED_HOSTS = []

# 📦 اپلیکیشن‌ها
INSTALLED_APPS = [
    "accounts.apps.AccountsConfig",
    "report.apps.ReportConfig",
    "blog.apps.BlogConfig",
    "main.apps.MainConfig",
    "notification.apps.NotificationConfig",

    # Third-party
    'django_jalali',
    'django_cleanup.apps.CleanupConfig',
    'jalali_date',
    'taggit',

    # Django default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "donation.apps.DonationConfig"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = "Razavieh.urls"

# 🎨 قالب‌ها
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Razavieh.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'Razavieh_db',
#         'USER': 'razavieh_user',
#         'PASSWORD': 'H0jat12(Ali):soon',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 📁 فایل‌های استاتیک و مدیا
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = '/images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'images')

# 🕒 تنظیمات عمومی
LANGUAGE_CODE = 'fa-ir'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 👤 مدل کاربر سفارشی
AUTH_USER_MODEL = 'accounts.CustomUser'

# 🔐 اعتبارسنجی رمز عبور
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 📨 تنظیمات ایمیل (برای بازیابی رمز)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'test.emial.django@gmail.com'
EMAIL_HOST_PASSWORD = 'qyupiaqlnpfgnvbf'

# 🔁 سشن‌ها
SESSION_COOKIE_AGE = 60 * 60 * 24 * 180  # 6 ماه
SESSION_SAVE_EVERY_REQUEST = True

# 📍 مسیر بعد از لاگین
LOGIN_REDIRECT_URL = '/report/report_list'

GHASEDAK_API_KEY = "97b761464896092337b2792e656b23382cd4b17561cceaccd1496ed68141b4aeyC6PCGMHHJGaZPpV"
