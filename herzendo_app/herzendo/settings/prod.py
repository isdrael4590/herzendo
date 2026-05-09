# No comprobar en ciertas líneas F403 y F405 para compartir las configuraciones del base.py
from .base import *  # noqa: F403

DEBUG = False
ADMINS = [("Fernando Jácome", "isdrael4590@gmail.com")]
ALLOWED_HOSTS += ["nginx"]
STATIC_ROOT = BASE_DIR / "static"  # noqa: F405
STATICFILES_DIRS = [
    BASE_DIR / "static",  # noqa: F405
]

STATIC_ROOT = BASE_DIR / "staticfiles"
# Configuraciones de seguridad
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True