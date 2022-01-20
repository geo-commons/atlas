import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG_DEFAULT = 'True'
SECRET_KEY_DEFAULT = 'changemetosomethingsecret' # noqa
ALLOWED_HOSTS_DEFAULT = 'localhost,127.0.0.1,[::1]'

if os.getenv('ATLAS_ENVIRONMENT') == 'production':
    DEBUG_DEFAULT = 'False'
    SECRET_KEY_DEFAULT = None
    ALLOWED_HOSTS_DEFAULT = ''

SECRET_KEY = os.getenv('SECRET_KEY', SECRET_KEY_DEFAULT)
DEBUG = os.getenv('DEBUG', DEBUG_DEFAULT) == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', ALLOWED_HOSTS_DEFAULT).split(',')
CTRIX_IPS = os.getenv('CTRIX_IPS', '*').split(',')

WFS_URL = os.getenv('WFS_URL', '')
WFS_URL_CTRIX = os.getenv('WFS_URL_CTRIX', '')

SMARTSTREET_USER = os.getenv('SMARTSTREET_USER', '')
SMARTSTREET_PASSWORD = os.getenv('SMARTSTREET_PASSWORD', '')
SMARTSTREET_API_KEY = os.getenv('SMARTSTREET_API_KEY', '')

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')

MATOMO_URL = os.getenv('MATOMO_URL', '')
MATOMO_SITE_ID = os.getenv('MATOMO_SITE_ID', '')

SENTRY_DSN = os.getenv('SENTRY_DSN', '')

AUTHENTICATION_ENABLE_CREDENTIALS = os.getenv('AUTHENTICATION_ENABLE_CREDENTIALS', 'True') == 'True'
AUTHENTICATION_ENABLE_OIDC = os.getenv('AUTHENTICATION_ENABLE_OIDC', 'False') == 'True'
OIDC_AD_ADD_AUTH_REQUEST_EXTRA_PARAMS = os.getenv('OIDC_AD_ADD_AUTH_REQUEST_EXTRA_PARAMS', 'False') == 'True'

OIDC_RP_CLIENT_ID = os.getenv('OIDC_CLIENT_ID', 'atlas')
OIDC_RP_CLIENT_SECRET = os.getenv('OIDC_CLIENT_SECRET', 'somethingsecret')
OIDC_RP_SIGN_ALGO = os.getenv('OIDC_SIGN_ALGO', 'RS256')
OIDC_RP_SCOPES = os.getenv('OIDC_SCOPES', 'openid email profile')
OIDC_OP_AUTHORIZATION_ENDPOINT = os.getenv('OIDC_AUTHORIZATION_ENDPOINT', 'http://localhost:6556/auth')
OIDC_OP_TOKEN_ENDPOINT = os.getenv('OIDC_TOKEN_ENDPOINT', 'http://localhost:6556/token')
OIDC_OP_USER_ENDPOINT = os.getenv('OIDC_USER_ENDPOINT', 'http://localhost:6556/userinfo')
OIDC_OP_JWKS_ENDPOINT = os.getenv('OIDC_JWKS_ENDPOINT', 'http://localhost:6556/keys')

OIDC_USERNAME_CLAIM = os.getenv('OIDC_USERNAME_CLAIM', 'sub')
OIDC_ACTIVATE_ON_CREATE = os.getenv('OIDC_ACTIVATE_ON_CREATE', 'True')

if OIDC_AD_ADD_AUTH_REQUEST_EXTRA_PARAMS:
    OIDC_AUTH_REQUEST_EXTRA_PARAMS = {
        'resource': 'urn:microsoft:userinfo'
    }

OIDC_STORE_ACCESS_TOKEN = True

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
    'webservice',
    'user_management',
    'webpack_loader',
    'atlas.apps.CustomConstance',
    'constance.backends.database',
    'mozilla_django_oidc',
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
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'utils.middleware.check_access_admin',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if AUTHENTICATION_ENABLE_OIDC:
    MIDDLEWARE += [
        'mozilla_django_oidc.middleware.SessionRefresh',
    ]

ROOT_URLCONF = 'atlas.urls'

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
                'utils.context_processors.ctrix_context',
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
    AUTHENTICATION_BACKENDS.append('webservice.auth.AtlasOIDCAuthenticationBackend')

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

LANGUAGE_CODE = 'nl'
TIME_ZONE = 'CET'
USE_I18N = True
USE_L10N = False
USE_TZ = True

AUTH_USER_MODEL = 'user_management.AtlasUser'

STATIC_URL = '/atlas/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATS_FILE = os.path.join(BASE_DIR, 'ui', 'webpack-stats.json')
if 'test' in sys.argv:
    STATS_FILE = os.path.join(BASE_DIR, 'ui', 'webpack-stats-test.json')

WEBPACK_LOADER = {
    'DEFAULT': {
        'STATS_FILE': STATS_FILE,
    }
}

LOGIN_URL = '/atlas/accounts/login/'
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
        }
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
    'FAVICON_URL': ('', ('Configureer een eigen favicon via een URL\nbijv. http://www.organization.com/favicon.ico'))
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
    )
}
