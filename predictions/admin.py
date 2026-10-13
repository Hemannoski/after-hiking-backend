from django.contrib import admin
from .models import Prediction

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    """Configuration de l'interface d'administration pour le modèle Prediction."""

    # --- 1. AFFICHAGE DE LA LISTE ---
    list_display = [
        "randonnee",
        "vues_min", "vues_max",
        "taux_likes_min", "taux_likes_max",
        "taux_commentaires_min", "taux_commentaires_max",
        "abonnes_min", "abonnes_max",
        "version_modele"
    ]

    # Barre de recherche (pour retrouver la prédiction d'une rando par son nom)
    search_fields = [
        "randonnee__titre_randonnee"
    ]

    list_filter = [
        "date_creation",
        "version_modele",
        "randonnee__titre_randonnee"
    ]

    # Tri par défaut
    ordering = ["-date_creation"]

    # TOUS LES CHAMPS EN LECTURE SEULE
    # L'admin ne doit JAMAIS modifier manuellement les prédictions de l'IA
    readonly_fields = [
        "randonnee",
        "vues_min", "vues_max",
        "taux_likes_min", "taux_likes_max",
        "taux_commentaires_min", "taux_commentaires_max",
        "abonnes_min", "abonnes_max",
        "version_modele",
        "date_creation"
    ]

    # Pagination
    list_per_page = 25