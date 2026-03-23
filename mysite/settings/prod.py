"""
Production settings for mysite project.

This file imports all settings from base.py and overrides
settings specific to the production environment.
"""

from .base import *

# Override DEBUG for production
DEBUG = False

# ALLOWED_HOSTS must be set via environment variable in production
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True

# ดึงค่า CSRF_TRUSTED_ORIGINS จาก .env มาแปลงเป็น List
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])

# บอก Django ว่า Request ที่เข้ามาผ่าน Proxy (Cloudflare) เป็น HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
