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
