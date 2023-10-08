from datetime import timedelta
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG_DEFAULT = 'True'
DEBUG_API_PROXY_DEFAULT = 'http://localhost:8050/api/'
SECRET_KEY_DEFAULT = 'changemetosomethingsecret'  # noqa
ALLOWED_HOSTS_DEFAULT = 'localhost,127.0.0.1,[::1]'
DEFAULT_SESSION_COOKIE_SECURE = 'False'
DEFAULT_SESSION_EXPIRE_AT_BROWSER_CLOSE = 'False'
DEFAULT_SESSION_COOKIE_AGE = '1909600'  # 2 weeks

if os.getenv('ATLAS_ENVIRONMENT') == 'production':
    DEBUG_DEFAULT = 'False'
    DEBUG_API_PROXY_DEFAULT = ''
    SECRET_KEY_DEFAULT = None
    ALLOWED_HOSTS_DEFAULT = ''
    DEFAULT_SESSION_COOKIE_SECURE = 'True'
    DEFAULT_SESSION_EXPIRE_AT_BROWSER_CLOSE = 'True'
    DEFAULT_SESSION_COOKIE_AGE = '28800'  # 8 hours

SECRET_KEY = os.getenv('SECRET_KEY', SECRET_KEY_DEFAULT)
DEBUG = os.getenv('DEBUG', DEBUG_DEFAULT) == 'True'
DEBUG_API_PROXY = os.getenv('DEBUG_API_PROXY', DEBUG_API_PROXY_DEFAULT)

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', ALLOWED_HOSTS_DEFAULT).split(',')
INTERNAL_IPS = list(filter(None, os.getenv('INTERNAL_IPS', '').split(',')))
ADMIN_IPS = list(filter(None, os.getenv('ADMIN_IPS', '').split(',')))

SMARTSTREET_USER = os.getenv('SMARTSTREET_USER', '')
SMARTSTREET_PASSWORD = os.getenv('SMARTSTREET_PASSWORD', '')
SMARTSTREET_API_KEY = os.getenv('SMARTSTREET_API_KEY', '')

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')

MATOMO_URL = os.getenv('MATOMO_URL', '')
MATOMO_SITE_ID = os.getenv('MATOMO_SITE_ID', '')

SENTRY_DSN = os.getenv('SENTRY_DSN', '')

AUTHENTICATION_ENABLE_CREDENTIALS = os.getenv(
    'AUTHENTICATION_ENABLE_CREDENTIALS', 'True') == 'True'
AUTHENTICATION_ENABLE_OIDC = os.getenv(
    'AUTHENTICATION_ENABLE_OIDC', 'False') == 'True'
OIDC_AD_ADD_AUTH_REQUEST_EXTRA_PARAMS = os.getenv(
    'OIDC_AD_ADD_AUTH_REQUEST_EXTRA_PARAMS', 'False') == 'True'

OIDC_RP_CLIENT_ID = os.getenv('OIDC_CLIENT_ID', 'atlas')
OIDC_RP_CLIENT_SECRET = os.getenv('OIDC_CLIENT_SECRET', 'somethingsecret')
OIDC_RP_SIGN_ALGO = os.getenv('OIDC_SIGN_ALGO', 'RS256')
OIDC_RP_SCOPES = os.getenv('OIDC_SCOPES', 'openid email profile')
OIDC_OP_AUTHORIZATION_ENDPOINT = os.getenv(
    'OIDC_AUTHORIZATION_ENDPOINT', 'http://localhost:6556/auth')
OIDC_OP_TOKEN_ENDPOINT = os.getenv(
    'OIDC_TOKEN_ENDPOINT', 'http://localhost:6556/token')
OIDC_OP_USER_ENDPOINT = os.getenv(
    'OIDC_USER_ENDPOINT', 'http://localhost:6556/userinfo')
OIDC_OP_JWKS_ENDPOINT = os.getenv(
    'OIDC_JWKS_ENDPOINT', 'http://localhost:6556/keys')

OIDC_USERNAME_CLAIM = os.getenv('OIDC_USERNAME_CLAIM', 'sub')
OIDC_ACTIVATE_ON_CREATE = os.getenv(
    'OIDC_ACTIVATE_ON_CREATE', 'True') == 'True'
OIDC_SYNC_GROUPS = os.getenv('OIDC_SYNC_GROUPS', 'False') == 'True'

if OIDC_AD_ADD_AUTH_REQUEST_EXTRA_PARAMS:
    OIDC_AUTH_REQUEST_EXTRA_PARAMS = {
        'resource': 'urn:microsoft:userinfo'
    }

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'USER': os.getenv('DB_USER', 'atlas'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'atlas'),
        'NAME': os.getenv('DB_NAME', 'atlas'),
        'CONN_MAX_AGE': 600,
    }
}

INSTALLED_APPS = [
    'homepage',
    'tables',
    'webservice',
    'portal',
    'user_management',
    'webpack_loader',
    'atlas.apps.CustomConstance',
    'constance.backends.database',
    'mozilla_django_oidc',
    'rest_framework',
    'django_filters',
    'import_export',
    'reversion',
    'revproxy',
    'debug_toolbar',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'utils.middleware.check_access_admin',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda r: os.getenv(
        'SHOW_DJANGO_DEBUG_TOOLBAR', 'False') == 'True'
}

if AUTHENTICATION_ENABLE_OIDC:
    MIDDLEWARE += [
        'utils.middleware.LogoutWhenOIDCTokenIsExpiredMiddleware'
    ]

ROOT_URLCONF = 'atlas.urls'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ]
}

SIMPLE_JWT = {
    # The Javascript frontend requests new tokens every 5 minutes
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=7),
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'constance.context_processors.config',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'utils.context_processors.global_settings',
                'utils.context_processors.homepage',
            ],
        },
    },
]

WSGI_APPLICATION = 'atlas.wsgi.application'

LAYER_CHOICES = (
    ('base_layer', 'Achtergrond kaart'),
    ('base_registration', 'Basis registratie'),
    ('theme_layer', 'Thema kaart'),
)

LAYER_CHOICES_RETURN_VALUES = {
    'theme_layer': 'themelayer:true',
    'base_registration': 'basisreg:true',
    'base_layer': 'isBaseLayer:true'
}

AUTHENTICATION_BACKENDS = []

if AUTHENTICATION_ENABLE_CREDENTIALS:
    AUTHENTICATION_BACKENDS.append('django.contrib.auth.backends.ModelBackend')

if AUTHENTICATION_ENABLE_OIDC:
    AUTHENTICATION_BACKENDS.append(
        'webservice.auth.AtlasOIDCAuthenticationBackend')

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

SESSION_COOKIE_NAME = 'atlas_session'
SESSION_COOKIE_SAMESITE = os.getenv('SESSION_COOKIE_SAMESITE', 'Lax')
SESSION_COOKIE_SECURE = os.getenv(
    'SESSION_COOKIE_SECURE', DEFAULT_SESSION_COOKIE_SECURE) == 'True'
SESSION_EXPIRE_AT_BROWSER_CLOSE = os.getenv(
    'SESSION_EXPIRE_AT_BROWSER_CLOSE', DEFAULT_SESSION_EXPIRE_AT_BROWSER_CLOSE) == 'True'
SESSION_COOKIE_AGE = int(os.getenv(
    'SESSION_COOKIE_AGE', DEFAULT_SESSION_COOKIE_AGE))

LANGUAGE_CODE = 'nl'
TIME_ZONE = 'Europe/Amsterdam'
USE_I18N = True
USE_L10N = False
USE_TZ = True

AUTH_USER_MODEL = 'user_management.AtlasUser'

STATIC_URL = '/atlas/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/atlas/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATS_FILE = os.path.join(BASE_DIR, 'ui', 'webpack-stats.json')
if 'test' in sys.argv:
    STATS_FILE = os.path.join(BASE_DIR, 'ui', 'webpack-stats-test.json')

WEBPACK_LOADER = {
    'DEFAULT': {
        'STATS_FILE': STATS_FILE,
    }
}

LOGIN_URL = '/atlas/login'
LOGIN_REDIRECT_URL = '/atlas/'
LOGOUT_REDIRECT_URL = '/atlas/'
LOGIN_REDIRECT_URL_FAILURE = '/atlas/login/failure'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'mozilla_django_oidc': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
    }
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG = {
    'ORGANIZATION_NAME': ('Gemeente Purmerend', 'De naam van de organisatie'),
    'DISCLAIMER': ('', 'Inhoud van de disclaimer die getoond wordt'),
    'POSITION_ZOOM': (13, 'Het zoomniveau van de opstartpositie'),
    'POSITION_CENTER_X': (126910, 'Het centrum X-coordinaat van de opstartpositie'),
    'POSITION_CENTER_Y': (505834, 'Het centrum Y-coordinaat van de opstartpositie'),
    'SUGGEST_MUNICIPALITIES': ('purmerend,beemster', 'Een komma-gescheiden lijst van gemeenten om adressen in te zoeken (voor auto-aanvulfunctionaliteit)'),
    'FAVICON_URL': ('', ('Configureer een eigen favicon via een URL\nbijv. http://www.organization.com/favicon.ico')),
    'MATOMO_URL': ('', ('Configureer de URL van Matomo om statistieken bij te houden')),
    'MATOMO_SITE_ID': ('', ('Configureer het site ID van Matomo om statistieken bij te houden')),
    'FEATURE_PORTAL': (False, ('Portaalfunctionaliteit')),
    'FEATURE_PRINT': (False, ('Printfunctionaliteit')),
    'FEATURE_DRAW': (False, ('Tekenfunctionaliteit')),
}

CONSTANCE_CONFIG_FIELDSETS = {
    '1. Organisatie': (
        'ORGANIZATION_NAME',
        'FAVICON_URL',
        'DISCLAIMER'
    ),
    '2. Kaartconfiguratie': (
        'POSITION_CENTER_X',
        'POSITION_CENTER_Y',
        'POSITION_ZOOM',
        'SUGGEST_MUNICIPALITIES'
    ),
    '3. Matomo': (
        'MATOMO_URL',
        'MATOMO_SITE_ID'
    ),
    '4. Features': (
        'FEATURE_PORTAL',
        'FEATURE_PRINT',
        'FEATURE_DRAW'
    )
}
