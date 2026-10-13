from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Configuration de l'interface d'administration pour le modèle Notification."""

    # --- 1. AFFICHAGE DE LA LISTE ---
    list_display = [
        "destinataire",
        "type_notification",
        "declencheur",
        "randonnee",
        "lue",
        "date_notification"
    ]

    # Filtres latéraux (très utile pour voir le backlog de notifs non lues)
    list_filter = [
        "lue",
        "type_notification"
    ]

    # Barre de recherche (pour retrouver les notifs d'un utilisateur précis)
    search_fields = [
        "destinataire__email",
        "declencheur__email"
    ]

    # Tri par défaut (les plus récentes en haut)
    ordering = ["-date_notification"]

    # Champs en lecture seule (l'historique ne se modifie pas)
    readonly_fields = [
        "date_notification"
    ]

    # Pagination
    list_per_page = 25