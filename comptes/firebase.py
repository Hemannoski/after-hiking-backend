from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed


def verifier_jeton_firebase(request, verifier_revocation=False):
    """Lit le jeton Bearer de la requête et le vérifie auprès de Firebase.

    Renvoie le jeton décodé (un dict avec 'uid', 'email', ...),
    ou None si la requête ne contient pas de jeton Bearer.
    Lève AuthenticationFailed si le jeton est présent mais invalide.

    verifier_revocation=True ajoute un contrôle auprès de Firebase : compte
    existant, non désactivé, jeton non révoqué (un appel réseau de plus).
    """
    en_tete = get_authorization_header(request).split()

    if not en_tete or en_tete[0].lower() != b'bearer':
        return None

    if len(en_tete) != 2:
        raise AuthenticationFailed("En-tête Authorization invalide.")

    try:
        jeton = en_tete[1].decode()
    except UnicodeError:
        raise AuthenticationFailed("En-tête Authorization invalide.")

    try:
        return auth.verify_id_token(jeton, check_revoked=verifier_revocation)
    except (ValueError, FirebaseError):
        raise AuthenticationFailed("Jeton Firebase invalide ou expiré.")


def supprimer_compte_firebase(uid):
    """Supprime le compte Firebase. Ne fait rien s'il n'existe déjà plus."""
    try:
        auth.delete_user(uid)
    except auth.UserNotFoundError:
        pass