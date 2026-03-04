from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

from .databases import *
from .installed_apps import *
from .middleware import *
from .rest_framework import *
from .cors import *
from .auth import *
from .static import *
from .templates import *


# Common Django settings
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = False
ALLOWED_HOSTS = []
ROOT_URLCONF = 'configs.urls'
WSGI_APPLICATION = 'configs.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
APPEND_SLASH = False
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'