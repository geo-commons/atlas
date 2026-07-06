import os
import sys
from datetime import timedelta
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG_DEFAULT = 'True'
DEBUG_API_PROXY_DEFAULT = 'http://localhost:8050/api/'
SECRET_KEY_DEFAULT = 'changemetosomethingsecret'  # noqa
ALLOWED_HOSTS_DEFAULT = 'localhost,127.0.0.1,[::1],host.docker.internal'
DEFAULT_SESSION_COOKIE_SECURE = 'False'
DEFAULT_SESSION_EXPIRE_AT_BROWSER_CLOSE = 'False'
DEFAULT_SESSION_COOKIE_AGE = '1909600'  # 2 weeks

if os.getenv('USE_SAFE_SETTINGS'):
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

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
RUNNING_TESTS = 'test' in sys.argv

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

SHOW_LAYERS_ONLY_WHEN_ACCESSIBLE = os.getenv(
    'SHOW_LAYERS_ONLY_WHEN_ACCESSIBLE', 'False') == 'True'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'USER': os.getenv('DB_USER', 'atlas'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'atlas'),
        'NAME': os.getenv('DB_NAME', 'atlas'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'CONN_MAX_AGE': 600,
    }
}

INSTALLED_APPS = [
    'homepage',
    'tables',
    'table',
    'webservice',
    'portal',
    'user_management',
    'authz',
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
    'django_vite'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'utils.middleware.check_access_admin',
    'utils.middleware.disable_admin1',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if 'test' in sys.argv:
    DEBUG = False
    INSTALLED_APPS = [app for app in INSTALLED_APPS if app != "debug_toolbar"]
    MIDDLEWARE = [mw for mw in MIDDLEWARE if mw !=
                  "debug_toolbar.middleware.DebugToolbarMiddleware"]

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
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_PAGINATION_CLASS': 'webservice.pagination.StandardResultsSetPagination',
}

SIMPLE_JWT = {
    # The Javascript frontend requests new tokens every 5 minutes
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=7),
}

IMPORT_EXPORT_TMP_STORAGE_CLASS = 'import_export.tmp_storages.MediaStorage'

DATA_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024  # 50 MB

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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

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
        "OPTIONS": {
            "min_length": 24,
        },
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

# Save files using system's standard umask. This is required for network mounts like
# Azure Files as they do not implement a full-fledged permission system.
# See https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FILE_UPLOAD_PERMISSIONS
FILE_UPLOAD_PERMISSIONS = None

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

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

CONSTANCE_ADDITIONAL_FIELDS = {
    'image_field': ['atlas.fields.SVGAndImageFormField', {}]
}

CONSTANCE_CONFIG = {
    'ORGANIZATION_NAME': ('Gemeente Purmerend', 'De naam van de organisatie'),
    'ORGANIZATION_LOGO': ('', 'Logo van de organisatie', 'image_field'),
    'DISCLAIMER': ('', 'Inhoud van de disclaimer die getoond wordt'),
    'POSITION_ZOOM': (13, 'Het zoomniveau van de opstartpositie'),
    'POSITION_CENTER_X': (126910, 'Het centrum X-coordinaat van de opstartpositie'),
    'POSITION_CENTER_Y': (505834, 'Het centrum Y-coordinaat van de opstartpositie'),
    'SUGGEST_MUNICIPALITIES': ('purmerend,beemster', 'Een komma-gescheiden lijst van gemeenten om adressen in te zoeken (voor auto-aanvulfunctionaliteit)'),
    'SUGGEST_MUNICIPALITIES_BRK': ('purmerend,beemster',
                               'Een komma-gescheiden lijst van gemeenten om percelen in te zoeken (voor auto-aanvul functionaliteit). Het gaat hier om kadastrale gemeenten: https://standaarden.overheid.nl/owms/terms/KadastraleGemeente.html'),
    'SUGGEST_MUNICIPALITIES_BAG': ('purmerend,beemster',
                               'Een komma-gescheiden lijst van gemeenten om adressen in te zoeken (voor auto-aanvul functionaliteit). Het gaat hier om gemeenten: https://standaarden.overheid.nl/owms/4.0/doc/waardelijsten/overheid.gemeente'),
    'FAVICON_URL': ('', ('Configureer een eigen favicon via een URL\nbijv. http://www.organization.com/favicon.ico')),
    'MATOMO_URL': ('', ('Configureer de URL van Matomo om statistieken bij te houden')),
    'MATOMO_SITE_ID': ('', ('Configureer het site ID van Matomo om statistieken bij te houden')),
    'MAP_AREA': ('', ('Configureer een gebied dat standaard uitgelicht wordt op de kaart')),
    'FEATURE_PORTAL': (False, ('Portaalfunctionaliteit')),
    'FEATURE_PRINT': (False, ('Printfunctionaliteit')),
    'FEATURE_SORT_LAYER': (False, 'Sorteer kaartlagen in de viewer'),
    'FEATURE_DISABLE_ADMIN1': (False, ('Zet admin1 uit')),
    'FEATURE_NEW_TABLES': (False, ('Gebruik de nieuwe tabellen functionaliteit')),
    'FEATURE_OLD_LINKED_DATA_AND_TEMPLATE': (True, ('Gebruik de oude gekoppelde data en templates')),
    'FEATURE_LAYER_INTERNAL_VISIBILITY': (True, ('Interne zichtbaarheid lagen')),
    'ORGANIZATION_IMAGE': (
        '', 'Organisatie header afbeelding', 'image_field'),
    'ORGANIZATION_PRIMARY_COLOR': (
        '#000000', 'Primaire kleur van de organisatie.\n Note: voor nu alleen beschikbaar in HEX'),
    'ORGANIZATION_TITLE_COLOR': (
        '#000000', 'Titel kleur op het portaal. Leeg = overnemen van standaard. NB: voor nu alleen beschikbaar in HEX'),
    'ORGANIZATION_TEXT_COLOR': (
        '#000000', 'Tekst kleur op het portaal. Leeg = overnemen van standaard. NB: voor nu alleen beschikbaar in HEX'),
    'ORGANIZATION_INTRODUCTION': ('', 'Introductie tekst die wordt laten zien bovenaan de pagina'),
    'ORGANIZATION_HEADER': ('', 'Header tekst die bovenaan de portaal pagina zichtbaar is'),
    'COMPLEX_DATA_DISPLAY': ('panel', 'Met deze instelling configureer je hoe complexe data weergegeven wordt in de viewer. In een paneel (vanaf de zijkant) of in een popup (in het midden van het scherm).'),
}

CONSTANCE_CONFIG_FIELDSETS = {
    '1. Organisatie': (
        'ORGANIZATION_NAME',
        'ORGANIZATION_LOGO',
        'FAVICON_URL',
        'DISCLAIMER'
    ),
    '2. Kaartconfiguratie': (
        'POSITION_CENTER_X',
        'POSITION_CENTER_Y',
        'POSITION_ZOOM',
        'SUGGEST_MUNICIPALITIES',
        'SUGGEST_MUNICIPALITIES_BRK',
        'SUGGEST_MUNICIPALITIES_BAG',
        'MAP_AREA'
    ),
    '3. Matomo': (
        'MATOMO_URL',
        'MATOMO_SITE_ID'
    ),
    '4. Features': (
        'FEATURE_PORTAL',
        'FEATURE_PRINT',
        'FEATURE_SORT_LAYER',
        'FEATURE_DISABLE_ADMIN1',
        'FEATURE_NEW_TABLES',
        'FEATURE_OLD_LINKED_DATA_AND_TEMPLATE',
        'FEATURE_LAYER_INTERNAL_VISIBILITY',
    ),
    '5. Portaal configuratie': (
        'ORGANIZATION_IMAGE',
        'ORGANIZATION_PRIMARY_COLOR',
        'ORGANIZATION_TITLE_COLOR',
        'ORGANIZATION_TEXT_COLOR',
        'ORGANIZATION_INTRODUCTION',
        'ORGANIZATION_HEADER'
    ),
    '6. Stijl': (
        'COMPLEX_DATA_DISPLAY',
    )
}

DJANGO_VITE_DEV_MODE = DEBUG or RUNNING_TESTS
DJANGO_VITE_MANIFEST_PATH = os.path.join(
    BASE_DIR, 'homepage/static/dist/manifest.json')

BASE_DIR = Path(__file__).resolve().parent.parent

# Add the build.outDir from vite.config.mjs to STATICFILES_DIRS
# so that collectstatic can collect your compiled vite assets.
vite_dist_dir = BASE_DIR / "homepage/static/dist"
STATICFILES_DIRS = [vite_dist_dir] if vite_dist_dir.exists() else []
