from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .firebase import verifier_jeton_firebase
from .models import Utilisateur


class FirebaseAuthentication(BaseAuthentication):
    """
    Authentification DRF par jeton Firebase.
    Le jeton est vérifié par verifier_jeton_firebase, puis on retrouve
    l'utilisateur correspondant dans PostgreSQL grâce à son firebase_uid.
    """

    def authenticate(self, request):
        # 1. Lire et vérifier le jeton (None si la requête n'en contient pas)
        decoded_token = verifier_jeton_firebase(request)
        if decoded_token is None:
            return None  # pas de jeton : on laisse les permissions décider

        # 2. Récupérer l'identifiant Firebase de l'utilisateur
        firebase_uid = decoded_token.get('uid')
        if not firebase_uid:
            raise AuthenticationFailed("Jeton Firebase sans UID.")

        # 3. Chercher l'utilisateur dans notre base
        try:
            user = Utilisateur.objects.get(
                firebase_uid=firebase_uid,
                is_active=True,
                date_suppression__isnull=True,
            )
        except Utilisateur.DoesNotExist:
            raise AuthenticationFailed(
                "Utilisateur inconnu. Appelez d'abord POST /auth/firebase pour créer votre compte."
            )

        # 4. Le tuple (user, auth) attendu par DRF
        return (user, decoded_token)

    def authenticate_header(self, request):
        # Fait répondre 401 (et non 403) quand l'authentification échoue
        return 'Bearer'