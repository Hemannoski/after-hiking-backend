from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Utilisateur, Appareil


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
        "compte_prive"
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
                    "compte_prive"
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
                    "compte_prive",
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



@admin.register(Appareil)
class AppareilAdmin(admin.ModelAdmin):
    """
        Configuration de l'interface d'administration pour le modèle Appareil.
    """

    # Cette méthode va tronquer la chaine du jeton de notification pour garder 20 caractère pour mieux l'afficher dans l'espace admin
    def jeton_notification_court(self, obj):
        return obj.jeton_notification_appareil[:21] + "..." if len(obj.jeton_notification_appareil) > 20 else obj.jeton_notification_appareil

        # --- 1. AFFICHAGE DE LA LISTE DES APPAREIL ---
    
    # Colonnes affichées dans la liste
    list_display = [
        "type_appareil",
        "utilisateur",
        "jeton_notification_court",
        "date_connexion",
        "date_derniere_connexion"
    ]


    # Filtres latéraux (à droite de la liste)
    list_filter = [
        "type_appareil"
    ]

    # Barre de recherche en haut
    search_fields = [
        "utilisateur__nom_utilisateur"
    ]

    # Champs affichés en lecture seule (non modifiables)
    readonly_fields = [
        "jeton_notification_appareil",
        "date_connexion",
        "date_derniere_connexion"
    ]

    # Tri par défaut (du plus récent au plus ancien)
    ordering = ["-date_derniere_connexion"]

    # Pagination (nombre de randonnee par page)
    list_per_page = 25