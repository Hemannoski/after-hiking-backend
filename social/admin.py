from django.contrib import admin
from .models import Commentaire, Like, Abonnement, Blocage, Signalement

@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    """Configuration de l'interface d'administration pour le modèle Commentaire."""


    def texte_court(self, obj):
        return obj.texte[: 50] + "..." if len(obj.texte) > 50 else obj.texte
    texte_court.short_description = "Aperçu du commentaire"



    # --- 1. AFFICHAGE DE LA LISTE DES COMMENTAIRES ---

    list_display = [
        "texte_court",
        "randonnee",
        "commentateur",
        "date_creation_commentaire",
        "commentaire_parent",
        "masque"
    ]


    # Filtres latéraux (à droite de la liste)
    list_filter = [
        "date_creation_commentaire",
        "randonnee",
    ]

    # Barre de recherche en haut
    search_fields = [
        "texte",
        "commentateur__nom_utilisateur",
    ]

    # Tri par défaut (du plus récent au plus ancien)
    ordering = ["-date_creation_commentaire"]


    # Pagination (nombre de randonnee par page)
    list_per_page = 25
        



@admin.register(Signalement)
class SignalementAdmin(admin.ModelAdmin):
    """Configuration de l'interface d'administration pour le modèle Signalement."""


    # --- 1. AFFICHAGE DE LA LISTE DES Signalement ---

    list_display = [
        "type_signalement",
        "type_signalement_id",
        "signaleur",
        "motif_signale",
        "statut_signale",
        "date_signalement"
    ]


    # Filtres latéraux (à droite de la liste)
    list_filter = [
        "statut_signale",
        "type_signalement",
        "date_signalement"
    ]

    # Barre de recherche en haut
    search_fields = [
        "type_signalement",
    ]

    # Tri par défaut (du plus récent au plus ancien)
    ordering = ["-date_signalement"]


    # Pagination (nombre de Signalement par page)
    list_per_page = 25



@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """Configuration de l'interface d'administration pour le modèle Like."""


    # --- 1. AFFICHAGE DE LA LISTE DES LIKE ---

    list_display = [
        "auteur",
        "randonnee",
        "date_du_like",
    ]


    # Filtres latéraux (à droite de la liste)
    list_filter = [
        "randonnee",
        "date_du_like"
    ]

    # Barre de recherche en haut
    search_fields = [
        "randonnee__titre_randonnee",
    ]

    # Tri par défaut (du plus récent au plus ancien)
    ordering = ["-date_du_like"]


    # Pagination (nombre de Like par page)
    list_per_page = 25



@admin.register(Abonnement)
class AbonnementAdmin(admin.ModelAdmin):
    """Configuration de l'interface d'administration pour le modèle Abonnement."""


    # --- 1. AFFICHAGE DE LA LISTE DES ABONNEMENT ---

    list_display = [
        "abonne",
        "suivi",
        "date_abonnement",
    ]


    # Filtres latéraux (à droite de la liste)
    list_filter = [
        "suivi",
        "abonne",
        "date_abonnement"
    ]

    # Barre de recherche en haut
    search_fields = [
        "abonne__email",
        "suivi__email"
    ]

    # Tri par défaut (du plus récent au plus ancien)
    ordering = ["-date_abonnement"]


    # Pagination (nombre de Abonnement par page)
    list_per_page = 25


@admin.register(Blocage)
class BlocageAdmin(admin.ModelAdmin):
    """Configuration de l'interface d'administration pour le modèle Blocage."""


    # --- 1. AFFICHAGE DE LA LISTE DES BLOCAGE ---

    list_display = [
        "utilisateur_bloque",
        "utilisateur",
        "date_compte_bloque",
    ]


    # Filtres latéraux (à droite de la liste)
    list_filter = [
        "date_compte_bloque",
    ]

    # Barre de recherche en haut
    search_fields = [
        "utilisateur_bloque__email",
        "utilisateur__email"
    ]

    # Tri par défaut (du plus récent au plus ancien)
    ordering = ["-date_compte_bloque"]


    # Pagination (nombre de Blocage par page)
    list_per_page = 25
        