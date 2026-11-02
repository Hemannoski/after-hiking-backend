import logging

import cloudinary
import cloudinary.exceptions
import cloudinary.uploader
from django.conf import settings

logger = logging.getLogger(__name__)

DELAI_ENVOI = 20  # secondes avant d'abandonner un appel à Cloudinary


class StockageIndisponible(Exception):
    """Le service d'hébergement des images ne répond pas ou refuse l'envoi."""


def public_id_photo(utilisateur_id):
    """Emplacement fixe de la photo d'un utilisateur sur Cloudinary."""
    return f"{settings.PHOTO_PROFIL_DOSSIER}/{utilisateur_id}"


def envoyer_photo_profil(fichier, utilisateur):
    """Envoie la photo à Cloudinary et renvoie son URL publique (https).

    Le nom est fixé par le serveur à partir de l'identifiant de l'utilisateur :
    une nouvelle photo remplace donc l'ancienne au même emplacement.
    """
    try:
        resultat = cloudinary.uploader.upload(
            fichier,
            public_id=public_id_photo(utilisateur.pk),
            asset_folder=settings.PHOTO_PROFIL_DOSSIER,
            overwrite=True,
            invalidate=True,
            timeout=DELAI_ENVOI,
        )
    except cloudinary.exceptions.Error:
        logger.exception("Échec de l'envoi de la photo de profil (utilisateur %s)", utilisateur.pk)
        raise StockageIndisponible
    return resultat['secure_url']


def supprimer_photo_profil(utilisateur_id):
    """Supprime la photo de Cloudinary. Un échec est journalisé, jamais propagé."""
    try:
        cloudinary.uploader.destroy(
            public_id_photo(utilisateur_id),
            invalidate=True,
            timeout=DELAI_ENVOI,
        )
    except cloudinary.exceptions.Error:
        logger.exception("Échec de la suppression de la photo de profil (utilisateur %s)", utilisateur_id)