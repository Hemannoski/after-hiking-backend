from django.db import models

class TypeNotification(models.TextChoices):
    LIKE = "like", "Like"
    COMMENTAIRE = "commentaire", "Commentaire"
    NOUVEL_ABONNE = "nouvel_abonne", "Nouvel_Abonne"
    NOUVELLE_RANDONNEE = "nouvelle_randonnee", "Nouvelle_Randonnee"


class Notification(models.Model):
    """Modèle Notification"""

    destinataire = models.ForeignKey(
        'comptes.Utilisateur',
        on_delete=models.CASCADE,
        related_name='notifications_recus',
        help_text="Celui a qui la notification est envoyée"
    )

    declencheur = models.ForeignKey(
        'comptes.Utilisateur',
        on_delete=models.CASCADE,
        related_name='notifications_declenchees',
        help_text="Celui qui a déclenché la notification (vide si notification système)"
    )

    randonnee = models.ForeignKey(
        'randonnees.Randonnee',
        on_delete=models.CASCADE,
        related_name='notifications',
        blank=True,
        null=True,
        help_text="La randonnée liée à la notification (optionnel)"
    )

    type_notification = models.CharField(
        max_length=20,
        choices=TypeNotification.choices,
        help_text="Notification pour un commentaire, un like, une nouvelle randonnee, un nouvel abonnement"
    )

    lue = models.BooleanField(
        default=False,
        help_text="Notification envoyee lue ou non lue"
    )

    date_notification = models.DateTimeField(
        auto_now_add=True,
        help_text="Date de l'envoie de la notification"
    )

    class Meta:
        db_table = "notifications"
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-date_notification"]
        indexes = [
            models.Index(
            fields=["destinataire", "lue"],
            name="idx_notif_non_lue_utilisateur"
        )
        ]
    

    def __str__(self) -> str:
        return f"{self.type_notification} pour {self.destinataire.email}"
