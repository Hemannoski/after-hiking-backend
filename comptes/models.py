from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UtilisateurManager(BaseUserManager):
    """
    Manager personnalisé pour créer des utilisateurs.
    Gère le hachage des mots de passe pour l'admin et les utilisateurs Firebase.
    """

    def create_user(self, email, firebase_uid, nom_utilisateur, **extra_fields):
        """Crée et sauvegarde un utilisateur standard."""
        if not email:
            raise ValueError("L'email est obligatoire.")
        if not firebase_uid:
            raise ValueError("Le firebase_uid est obligatoire.")
        if not nom_utilisateur:
            raise ValueError("Le nom_utilisateur est obligatoire.")

        email = self.normalize_email(email)

        # 1. On extrait le mot de passe des champs supplémentaires (s'il existe)
        password = extra_fields.pop('password', None)

        utilisateur = self.model(
            email=email,
            firebase_uid=firebase_uid,
            nom_utilisateur=nom_utilisateur,
            **extra_fields,
        )

        # 2. C'EST ICI QUE LA MAGIE OPÈRE :
        if password:
            # Si un mot de passe est fourni (cas du superutilisateur admin), on le hache !
            utilisateur.set_password(password)
        else:
            # Si aucun mot de passe (cas d'un utilisateur créé via l'API/Firebase), 
            # on dit à Django que ce compte n'a pas de mot de passe utilisable.
            utilisateur.set_unusable_password()

        utilisateur.save(using=self._db)
        return utilisateur

    def create_superuser(self, email, firebase_uid, nom_utilisateur, **extra_fields):
        """Crée un superutilisateur (pour accéder à l'admin Django)."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # On s'assure que is_staff et is_superuser sont bien True pour un admin
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Le superutilisateur doit avoir is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Le superutilisateur doit avoir is_superuser=True.")

        return self.create_user(email, firebase_uid, nom_utilisateur, **extra_fields)


class Utilisateur(AbstractBaseUser, PermissionsMixin):
    """
    Modèle utilisateur personnalisé pour After Hiking.
    """

    # --- Champs d'identification et de profil ---
    firebase_uid = models.CharField(
        max_length=225,
        unique=True,
        help_text="Identifiant unique fourni par Firebase Auth."
    )
    email = models.EmailField(
        unique=True,
        help_text="Adresse email obligatoire (utilisée pour la connexion Firebase)."
    )
    nom_affiche = models.CharField(
        blank=True,
        default="",
        max_length=100,
        help_text="Nom affiché publiquement (ex: Awa Koné)."
    )
    nom_utilisateur = models.CharField(
        max_length=50,
        unique=True,
        help_text="Nom d'utilisateur unique (ex: @awa_hikes)."
    )
    bio = models.TextField(
        blank=True,
        default="",
        help_text="Courte description de l'utilisateur."
    )
    ville = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="Ville de résidence (utile pour l'IA et le filtrage)."
    )
    photo_profil = models.URLField(
        max_length=500,
        blank=True,
        default="",
        help_text="Lien vers la photo de profil hébergée dans le cloud."
    )

    # --- Dates ---
    date_creation = models.DateTimeField(
        auto_now_add=True,
        help_text="Date et heure de création du compte."
    )
    date_suppression = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date de suppression douce (soft delete)."
    )

    # --- Champs techniques Django (requis pour l'admin) ---
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(
        default=False,
        help_text="Indique si l'utilisateur peut accéder à l'admin Django."
    )

    compte_prive = models.BooleanField(
        default=False,
        help_text="Compte prive ou publique permmettant aux abonnés non bloqué de voir les randonnees publiées"
    )

    # --- Liaison avec le Manager personnalisé ---
    objects = UtilisateurManager()

    # --- Configuration Django ---
    # L'email devient l'identifiant principal pour la connexion
    USERNAME_FIELD = "email"
    # Les champs obligatoires lors de la création via le terminal (en plus de l'email)
    REQUIRED_FIELDS = ["firebase_uid", "nom_utilisateur"]

    class Meta:
        db_table = "utilisateurs"
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ["-date_creation"]

    def __str__(self):
        return self.nom_utilisateur





class TypeAppareil(models.TextChoices):
    ANDROID = 'android', 'Android'
    IOS = 'ios', 'Ios (Apple)'



class Appareil(models.Model):
    """Ce modèle gère les notifications que Firebase envoie aux utilisateurs sur leurs téléphones"""

    type_appareil = models.CharField(
        max_length=20, 
        choices=TypeAppareil.choices, 
        help_text="Le systeme d'exploitation du téléphone "
    )


    utilisateur = models.ForeignKey(
        'comptes.Utilisateur',
        on_delete=models.CASCADE,
        related_name='mes_appareils',
        help_text="Le propriétaire du téléphone"
    )


    jeton_notification_appareil = models.TextField(
        help_text="Le jeton de notification envoyé par firebase"
    )

    date_connexion = models.DateTimeField(
        auto_now_add=True,
        help_text="La date et l'heure de la prémière connexion de l'utilisateur"
    )

    date_derniere_connexion = models.DateTimeField(
        auto_now=True,
        help_text="La dernière date de connexion"
    )


    class Meta:
        db_table = "appareils"
        verbose_name = "Appareil"
        verbose_name_plural = "Appareils"
        ordering = ["-date_connexion"]
        constraints = [
            models.UniqueConstraint(fields=["utilisateur", "jeton_notification_appareil"],
            name="unique_jeton_par_utilisateur")
        ]

    def __str__(self) -> str:
        return f"{self.type_appareil} - {self.utilisateur.email}"
    
