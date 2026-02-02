"""
Development settings for mysite project.

This file imports all settings from base.py and overrides
settings specific to the development environment.
"""

from .base import *

# Override DEBUG for development
DEBUG = True

# Allow local development hosts
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]
