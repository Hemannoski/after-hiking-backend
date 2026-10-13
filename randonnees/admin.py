from django.contrib import admin
from .models import Randonnee, StatistiqueRandonnee

@admin.register(Randonnee)
class RandonneeAdmin(admin.ModelAdmin):
    """Configuration de l'interface d'administration pour le modèle Randonnee."""


    def apercu_couverture(self, obj):
        if obj.media_couverture:
            return f"{obj.media_couverture.type_media} - {obj.media_couverture.lien_photo[:30]}..."
        return "Aucune"
    apercu_couverture.short_description = "Aperçu du média de couverture"



    # --- 1. AFFICHAGE DE LA LISTE DES RANDONNEES ---

    list_display = [
        "titre_randonnee",
        "lieu_randonnee",
        "date_randonnee",
        "date_publication_randonnee",
        "distance_randonnee_km",
        "duree_randonnee_minutes",
        "status_randonnee",
        "niveau_difficulte_randonnee",
        "auteur",
        "apercu_couverture"
    ]

    # Colonnes cliquables pour trier
    list_display_links = [
        "lieu_randonnee", 
        "niveau_difficulte_randonnee", 
        "status_randonnee"
    ]

    # Filtres latéraux (à droite de la liste)
    list_filter = [
        "lieu_randonnee",
        "niveau_difficulte_randonnee",
        "status_randonnee",
        "date_publication_randonnee",
    ]

    # Barre de recherche en haut
    search_fields = [
        "lieu_randonnee",
        "titre_randonnee",
        "status_randonnee",
        "niveau_difficulte_randonnee",
        "auteur__nom_utilisateur"
    ]

    # Tri par défaut (du plus récent au plus ancien)
    ordering = ["-date_publication_randonnee"]

    # Champs affichés en lecture seule (non modifiables)
    readonly_fields = [
        "date_publication_randonnee",
        "date_randonnee",
    ]

    # Pagination (nombre de randonnee par page)
    list_per_page = 25

    # --- 3. FORMULAIRE DE MODIFICATION D'UNE RANDONNEE EXISTANTE ---
        # Ce formulaire est complet et organisé en sections
        
    fieldsets = (
        (
            "Informations générales",
            {
                "fields": (
                    "titre_randonnee",
                    "lieu_randonnee",
                    "description_randonnee",  
                ),
            },
        ),
        (
            "Caractéristiques techniques",
            {
                "fields": (
                    "duree_randonnee_minutes",
                    "niveau_difficulte_randonnee",
                    "latitude_coordonnee_randonnee",
                    "longitude_coordonnee_randonnee",
                    "distance_randonnee_km"
                ),
            },
        ),
        (
            "Médias et publications",
            {
                "fields": (
                    "media_couverture",
                    "status_randonnee",
                ),
            },
        ),
        (
            "Auteur",
            {
                "fields": (
                    "auteur",
                ),
            },
        ),
    )




@admin.register(StatistiqueRandonnee)
class StatistiqueRandonneeAdmin(admin.ModelAdmin):
    """Configuration de l'interface d'administration pour le modèle Statistique Randonnee."""

    # --- 1. AFFICHAGE DE LA LISTE DES STATISTIQUE RANDONNEE ---
        
    # Colonnes affichées dans la liste
    list_display = [
        "randonnee",
        "nombre_vues",
        "nombre_likes",
        "nombre_commentaires",
        "abonnes_auteur_a_la_publication",
        "nb_abonnes_gagnes",
        "nombre_medias",
        "longueur_description_randonnee",
        "date_creation_statistique",
        "date_derniere_mise_a_jour"
    ]

    # Filtres latéraux (à droite de la liste)
    list_filter = [
        "date_derniere_mise_a_jour",
        "date_creation_statistique",
    ]

    # Barre de recherche en haut
    search_fields = [
        "randonnee__titre_randonnee",
    ]

    # Tri par défaut (du plus récent au plus ancien)
    ordering = ["-date_creation_statistique"]

    # Champs affichés en lecture seule (non modifiables)
    readonly_fields = [
        "randonnee",
        "nombre_vues",
        "nombre_likes",
        "nombre_commentaires",
        "abonnes_auteur_a_la_publication",
        "nb_abonnes_gagnes",
        "date_creation_statistique",
        "date_derniere_mise_a_jour",
        "nombre_medias",
        "longueur_description_randonnee",
    ]

    # Pagination (nombre de randonnee par page)
    list_per_page = 25