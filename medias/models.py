from django.db import models

class TypeMedias(models.TextChoices):
    PHOTO = "photo", "Photo"
    VIDEO = "video", "Video"

class StatutTraitementDuMedia(models.TextChoices):
    EN_ATTENTE = "en_attente", "En Attente"
    PRET = "pret", "Prêt"
    ECHEC = "echec", "Echec"


class Media(models.Model):

    """Ce modèle est responsable de gérer les vidéos et photos des utilisateurs"""

    randonnee = models.ForeignKey(
        'randonnees.Randonnee',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='tous_mes_medias',
        help_text="La clé étrangère de la randonnée qui a été publiée"
    )

    type_media = models.CharField(
        max_length=10,
        blank=True,
        choices=TypeMedias.choices,
        default=TypeMedias.PHOTO,
        help_text="Le type du média téléchargé"
    )

    url_media = models.URLField(
        max_length=500,
        help_text="Le lien du média (la photo ou vidéo) de la randonnée hébergé sur le cloud."                
    )

    identifiant_mux = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        help_text="L'identifiant technique de la vidéo (uniquement pour les vidéos Mux)."
    )

    duree_video_en_seconde = models.IntegerField(
        help_text="Le temps que fait la vidéo en seconde uniquement pour les vidéos", 
        blank=True, 
        null=True
    )

    taille_en_octet = models.BigIntegerField(help_text="La taille de la vidéo ou de la photo en octet")

    ordre = models.PositiveIntegerField(default=0, help_text="L'ordre d'affichage du média dans la galerie.")

    status_traitement = models.CharField(
        max_length=20,
        blank=True,
        choices=StatutTraitementDuMedia.choices,
        default=StatutTraitementDuMedia.EN_ATTENTE,
        help_text="Le status du traitement du media (uploade, compression, etc.)."
    )

    class Meta:
        db_table = "medias"
        verbose_name = "Média"
        verbose_name_plural = "Médias"
        ordering = ["ordre", "-id"]

    def __str__(self) -> str:
        return f"{self.type_media} - Randonnée {self.randonnee}"

