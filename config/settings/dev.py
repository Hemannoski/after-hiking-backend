"""
Réglages spécifiques au développement local.
Hérite de tous les réglages de base.py.
"""

from .base import *

# Activation du mode débogage (détails des erreurs, etc.)
DEBUG = True

# Ajout de Django Debug Toolbar
INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Nécessaire pour que la toolbar s'affiche correctement sur localhost
INTERNAL_IPS = [
    "127.0.0.1",
]

# En développement, on affiche les requêtes SQL dans la console pour le débogage
LOGGING = {
    'version': 1,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
}