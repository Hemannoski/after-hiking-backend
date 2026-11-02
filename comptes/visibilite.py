from django.db.models import Exists, OuterRef

from social.models import Abonnement

from .models import Utilisateur


def utilisateurs_visibles(moi):
    """Utilisateurs que `moi` a le droit de voir.

    Comptes actifs, sans blocage dans un sens ou dans l'autre. Chaque utilisateur
    est annoté de `suivi_par_moi` (vrai si `moi` le suit).
    """
    return (
        Utilisateur.objects
        .filter(is_active=True, date_suppression__isnull=True)
        .exclude(bloque_par__utilisateur=moi)             # je l'ai bloqué
        .exclude(mes_blocages__utilisateur_bloque=moi)    # il m'a bloqué
        .annotate(
            suivi_par_moi=Exists(
                Abonnement.objects.filter(abonne=moi, suivi=OuterRef('pk'))
            ),
        )
    )