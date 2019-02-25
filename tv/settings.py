"""
Django settings for tv project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Application definition

CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_ALLOW_ALL = False
# CORS_ORIGIN_WHITELIST: specify a list of origin hostnames that are authorized to make a cross-site HTTP request
# Example:

# CORS_ORIGIN_WHITELIST = (
#     'google.com',
#     'hostname.example.com'
# )
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tv.urls'

WSGI_APPLICATION = 'tv.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# this is the dejavu database config
DB_ENGINE = 'django.db.backends.mysql'
DATABASES = {
    'default': {
        'ENGINE': DB_ENGINE, 
        'NAME': 'dejavu',
        'USER': 'dejavu',
        'PASSWORD': 'tvsnax',
        'HOST': '93.152.136.117',
        'PORT': '3306',
    }
}
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = False # we dont need timeaware datetime compares!
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
# DATETIME_INPUT_FORMATS = (
#     '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
#     '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
#     '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
#     # '%Y-%m-%d',              # '2006-10-25'
#     '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
#     '%m/%d/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
#     '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
#     # '%m/%d/%Y',              # '10/25/2006'
#     '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
#     '%m/%d/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
#     '%m/%d/%y %H:%M',        # '10/25/06 14:30'
#     # '%m/%d/%y',              # '10/25/06'
# )

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

INSTALLED_APPS = (
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    # 'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    'django.contrib.staticfiles',
    # https://github.com/ottoyiu/django-cors-headers
    'corsheaders',
    # 'custom_user',
    'rest_framework',
    # http://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
    # 'rest_framework.authtoken', # requires https!!!
    'recognition',
    'users',
    'admindb',
    'programs',
    'prizes',
)

AUTH_USER_MODEL = 'users.Users'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# http://www.django-rest-framework.org/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'lgl9m5z!#7c&v8++-8f14bnoqusw91c7v$h-j6y&1rf11jxd$s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

MEDIA_ROOT = "d:/tmp/"
TIMEOUT = 600 #the default one: works well for a 2 minute file

# $$$ if you receive this error: just increase the timeout time:
# $$$error: [Errno 10053] An established connection was aborted by the software in your request
# $$$settings.TIMEOUT would have no influence on that upload error

# read more information @ https://docs.djangoproject.com/en/1.7/ref/settings/
ALLOWED_HOSTS = ["192.168.0.1"]
ALLOWED_HOSTS = ["localhost", "127.0.0.1","93.152.136.117"]

## dejavu
RECOGNIZABLE_EXTENSIONS = ["wav", "mp3", "ogg", "flv"]
RECOGNITION_MINIMUM = 100
DJV_CONF = "dejavu/dejavu.cnf"
# FILTER_USER_PRIZES_THROUGH_PRIZE
# if true:   self.user_prizes.filter(user_id=user.id)
# if false:  user.user_prizes.filter(prize_id=self.id)
FILTER_USER_PRIZES_THROUGH_PRIZE = True
ADMINS_REMOTE_ADDRESSES = ["127.0.0.1",
    "93.152.136.117", # isko
    "78.90.13.11", #dichev
] #for fingerprinting

# https://docs.djangoproject.com/en/1.7/ref/settings/#admins
# ADMINS = (('Isko', 'iskren.jgd@gmail.com'),)
# Note that Django will email all of these people whenever an error happens. 


# https://docs.djangoproject.com/en/1.7/ref/settings/#std:setting-FILE_UPLOAD_HANDLERS
FILE_UPLOAD_HANDLERS = (
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
    )

APPEND_SLASH=False

# guidelines
#http://www.django-rest-framework.org/api-guide/settings/
# check defaults here
#https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/settings.py
REST_FRAMEWORK = {
    'UNICODE_JSON': True,
    'COMPACT_JSON': True,
    'UPLOADED_FILES_USE_URL': False,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    "DEFAULT_RENDERER_CLASSES": (
        'rest_framework.renderers.JSONRenderer',#for production
    ),
    "DEFAULT_PARSER_CLASSES": (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
}

# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

JWT_AUTH = {
    # 'JWT_ENCODE_HANDLER':
    # 'rest_framework_jwt.utils.jwt_encode_handler',

    # 'JWT_DECODE_HANDLER':
    # 'rest_framework_jwt.utils.jwt_decode_handler',

    # 'JWT_PAYLOAD_HANDLER':
    # 'rest_framework_jwt.utils.jwt_payload_handler',

    # 'JWT_PAYLOAD_GET_USER_ID_HANDLER':
    # 'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

    'JWT_RESPONSE_PAYLOAD_HANDLER': 'authentication.utils.jwt_response_payload_handler',

    # 'JWT_SECRET_KEY': settings.SECRET_KEY,# the one above
    # 'JWT_ALGORITHM': 'HS256',
    # 'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': False, #unlimited session
    # 'JWT_LEEWAY': 0,
    # 'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300),

    # 'JWT_ALLOW_REFRESH': False,
    # 'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

    # 'JWT_AUTH_HEADER_PREFIX': 'JWT',
}