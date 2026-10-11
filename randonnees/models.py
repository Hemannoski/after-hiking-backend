from django.db import models

class StatutRandonnee(models.TextChoices):
    BROUILLON = "brouillon", "Brouillon"
    PUBLIE = "publie", "Publié"
    MASQUE = "masque", "Masqué"

class DifficulteRandonnee(models.TextChoices):
    FACILE = "facile", "Facile"
    MOYEN = "moyen", "Moyen"
    DIFFICILE = "difficile", "Difficile"


class Randonnee(models.Model):

    """modèle randonnee"""

    auteur = models.ForeignKey(
        'comptes.Utilisateur', 
        on_delete=models.CASCADE,
        help_text="La clé étrangère de la personne qui a publié la randonnée."
    )

    media_couverture = models.ForeignKey(
        'medias.Media', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='randos_avec_cette_couverture',
        help_text="La clé étrangère de la photo ou de la vidéo mise en avant sur la publication de la randonnée."
    )

    titre_randonnee = models.CharField(
        max_length=255,
        help_text="Le titre de la randonnée."    
    )

    lieu_randonnee = models.CharField(
        max_length=50,
        help_text="Le lieu où s'est tenu la randonnée."
    )

    latitude_coordonnee_randonnee = models.DecimalField(
        blank=True, 
        null=True, 
        max_digits=9, 
        decimal_places=6,
        help_text="La latitude du lieu de la randonnée."
    )

    longitude_coordonnee_randonnee = models.DecimalField(
        blank=True, 
        null=True, 
        max_digits=9, 
        decimal_places=6,
        help_text="La longitude du lieu de la randonnée."
    )

    date_randonnee = models.DateField(
        blank=True, 
        null=True,
        help_text="La date de la randonnée."
    )

    date_publication_randonnee = models.DateTimeField(
        blank=True, 
        null=True,
        help_text="La date de publication de la randonnée."
    )

    status_randonnee = models.CharField(
        max_length=10, 
        choices=StatutRandonnee.choices, 
        default=StatutRandonnee.BROUILLON,
        help_text="Le statut de la randonnée est il en mode publié, masqué ou brouillon?."
    )

    distance_randonnee_km = models.FloatField(help_text="Distance totale en kilomètres.")

    duree_randonnee_minutes = models.IntegerField(help_text="La durée estimée de la randonnée en minutes.")

    description_randonnee = models.TextField(help_text="La description de la randonnée.")

    niveau_difficulte_randonnee = models.CharField(
        max_length=10, 
        choices=DifficulteRandonnee.choices, 
        default=DifficulteRandonnee.FACILE,
        help_text="Le niveau de difficulté de la randonnée."
    )


    class Meta:
        db_table = "randonnees"
        verbose_name = "Randonnee"
        verbose_name_plural = "Randonnees"
        ordering = ["-date_publication_randonnee"]

    def __str__(self):
        return self.titre_randonnee

