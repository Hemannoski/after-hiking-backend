from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Utilisateur


@admin.register(Utilisateur)
class UtilisateurAdmin(BaseUserAdmin):
    """
    Configuration de l'interface d'administration pour le modèle Utilisateur.
    On hérite de BaseUserAdmin pour bénéficier des fonctionnalités natives de Django
    (gestion des permissions, groupes, etc.).
    """

    # --- 1. AFFICHAGE DE LA LISTE DES UTILISATEURS ---
    
    # Colonnes affichées dans la liste
    list_display = [
        "email",
        "nom_utilisateur",
        "nom_affiche",
        "ville",
        "is_active",
        "is_staff",
        "date_creation",
    ]
    
    # Colonnes cliquables pour trier
    list_display_links = ["email", "nom_utilisateur"]
    
    # Filtres latéraux (à droite de la liste)
    list_filter = [
        "is_active",
        "is_staff",
        "ville",
        "date_creation",
    ]
    
    # Barre de recherche en haut
    search_fields = [
        "email",
        "nom_utilisateur",
        "nom_affiche",
        "firebase_uid",
    ]
    
    # Pagination (nombre d'utilisateurs par page)
    list_per_page = 25
    
    # Tri par défaut (du plus récent au plus ancien)
    ordering = ["-date_creation"]

    # Champs affichés en lecture seule (non modifiables)
    readonly_fields = [
        "last_login",
        "date_creation",
    ]


    # --- 2. FORMULAIRE DE CRÉATION D'UN NOUVEL UTILISATEUR ---
    # Ce formulaire est simplifié : on ne demande que l'essentiel
    
    add_fieldsets = (
        (
            "Identifiants de connexion",
            {
                "classes": ("wide",),  # Classe CSS pour un formulaire plus large
                "fields": (
                    "email",
                    "firebase_uid",
                    "nom_utilisateur",
                    "password1",  # Champ mot de passe (géré par Django)
                    "password2",  # Confirmation du mot de passe
                ),
            },
        ),
    )


    # --- 3. FORMULAIRE DE MODIFICATION D'UN UTILISATEUR EXISTANT ---
    # Ce formulaire est complet et organisé en sections
    
    fieldsets = (
        (
            "Informations de connexion",
            {
                "fields": (
                    "email",
                    "firebase_uid",
                    "password",  # Lien "Changer le mot de passe"
                ),
            },
        ),
        (
            "Profil public",
            {
                "fields": (
                    "nom_affiche",
                    "nom_utilisateur",
                    "bio",
                    "photo_profil",
                    "ville",
                ),
            },
        ),
        (
            "Permissions et droits",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",  # Groupes Django (hérité de PermissionsMixin)
                    "user_permissions",  # Permissions Django (hérité de PermissionsMixin)
                ),
            },
        ),
        (
            "Dates importantes",
            {
                "fields": (
                    "last_login",  # Hérité de AbstractBaseUser
                    "date_suppression",
                ),
            },
        ),
    )