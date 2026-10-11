from django.contrib import admin
from .models import Media

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    """Configuration de l'interface d'administration pour le modèle Média."""

    # --- 1. AFFICHAGE DE LA LISTE DES MEDIAS ---

    list_display = [
        "type_media",
        "randonnee",
        "taille_en_octet",
        "status_traitement",
        "url_media",
        "identifiant_mux",
        "duree_video_en_seconde"
    ]

    # Colonnes cliquables pour trier
    list_display_links = [
        "type_media", 
        "taille_en_octet", 
    ]

    # Filtres latéraux (à droite de la liste)
    list_filter = [
        "type_media",
        "status_traitement",
        "randonnee",
    ]

    # Barre de recherche en haut
    search_fields = [
        "type_media",
        "status_traitement",
        "taille_en_octet",
    ]

    # Tri par défaut (du plus récent au plus ancien)
    ordering = ["ordre"]

    # Champs affichés en lecture seule (non modifiables)
    readonly_fields = [
        "type_media"
    ]

    # Pagination (nombre de randonnee par page)
    list_per_page = 25

    # --- 3. FORMULAIRE DE MODIFICATION D'UN MEDIA EXISTANT ---
        # Ce formulaire est complet et organisé en sections
        
    fieldsets = (
        (
            "Informations du fichier",
            {
                "fields": (
                    "url_media",
                    "taille_en_octet",  
                ),
            },
        ),
        (
            "Lien avec la randonnee",
            {
                "fields": (
                    "randonnee",
                    "ordre",
                ),
            },
        ),
        (
            "Traitement",
            {
                "fields": (
                    "status_traitement",
                    "identifiant_mux",
                    "duree_video_en_seconde",
                ),
            },
        ),
    )