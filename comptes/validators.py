from django.conf import settings
from PIL import Image, UnidentifiedImageError
from rest_framework.exceptions import ValidationError

DIMENSION_MAX = 4096  # pixels, largeur et hauteur


def valider_photo_profil(fichier):
    """Valide une photo de profil envoyée par le client.

    Ne fait que vérifier : lève ValidationError si le fichier est refusé,
    ne renvoie rien sinon. Le fichier est rembobiné à la fin pour pouvoir
    être relu (envoi à Cloudinary).
    """
    # 1. Taille : contrôlée avant d'ouvrir l'image
    if fichier.size > settings.PHOTO_PROFIL_TAILLE_MAX:
        taille_max_mo = settings.PHOTO_PROFIL_TAILLE_MAX // (1024 * 1024)
        raise ValidationError(f"L'image est trop lourde (maximum {taille_max_mo} Mo).")

    try:
        with Image.open(fichier) as image:
            # 2. Format réel, lu dans le contenu et non dans l'extension
            type_reel = Image.MIME.get(image.format or '')
            if type_reel not in settings.PHOTO_PROFIL_TYPES_ACCEPTES:
                raise ValidationError("Format refusé : utilisez une image JPEG, PNG ou WebP.")

            # 3. Dimensions (lues dans l'en-tête, sans décoder toute l'image)
            largeur, hauteur = image.size
            if largeur > DIMENSION_MAX or hauteur > DIMENSION_MAX:
                raise ValidationError(
                    f"L'image est trop grande (maximum {DIMENSION_MAX} x {DIMENSION_MAX} pixels)."
                )

            # 4. Intégrité du fichier
            image.verify()
    except ValidationError:
        raise
    except (UnidentifiedImageError, Image.DecompressionBombError, OSError, SyntaxError, ValueError):
        raise ValidationError("Le fichier n'est pas une image valide.")
    finally:
        fichier.seek(0)