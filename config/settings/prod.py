"""
Réglages spécifiques à la production.
Hérite de tous les réglages de base.py.
"""

from .base import *

# Désactivation absolue du mode débogage en production
DEBUG = False

# Sécurité renforcée pour les connexions HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Note : La SECRET_KEY, les accès DB, etc. seront lus depuis 
# les variables d'environnement de ton serveur de production.