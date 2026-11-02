import random
import re
import unicodedata

from .models import Utilisateur

NB_CHIFFRES = 5
LONGUEUR_MAX = 50
LONGUEUR_BASE_MAX = LONGUEUR_MAX - 1 - NB_CHIFFRES  # 44


def nettoyer(texte):
    """Met un texte en forme : 'Awa Koné' -> 'awa_kone'."""
    texte = unicodedata.normalize('NFKD', texte)
    texte = texte.encode('ascii', 'ignore').decode('ascii')
    texte = re.sub(r'[^a-z0-9]+', '_', texte.lower())
    return texte.strip('_')[:LONGUEUR_BASE_MAX].strip('_')


def generer_nom_utilisateur(nom_complet, email=''):
    """Génère un nom libre : @ + nom mis en forme + 5 chiffres."""
    base = nettoyer(nom_complet) or nettoyer(email.split('@')[0]) or 'utilisateur'
    for _ in range(20):
        candidat = f"@{base}{random.randint(0, 10**NB_CHIFFRES - 1):0{NB_CHIFFRES}d}"
        if not Utilisateur.objects.filter(nom_utilisateur=candidat).exists():
            return candidat
    raise RuntimeError("Impossible de générer un nom d'utilisateur libre.")


def choisir_nom_utilisateur(propose, nom_complet, email=''):
    """Garde le nom proposé par l'application s'il est libre, sinon en génère un."""
    if propose and not Utilisateur.objects.filter(nom_utilisateur=propose).exists():
        return propose
    return generer_nom_utilisateur(nom_complet, email)