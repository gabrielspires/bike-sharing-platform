from .base import *

DEBUG = True
MAILERS["default"]["BACKEND"] = "django.core.mail.backends.console.EmailBackend"
