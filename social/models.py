from django.core.exceptions import ValidationError
from django.db import models


class Commentaire(models.Model):
    """Ce modèle gères tous les commentaires des utilisateurs"""

    randonnee_id: int
    commentaire_parent_id: int | None

    randonnee = models.ForeignKey(
        'randonnees.Randonnee',
        on_delete=models.CASCADE,
        related_name='commentaires',
        help_text="L'identifiant de la randonnée auquel appartient ce commentaire"
    )

    commentateur = models.ForeignKey(
        'comptes.Utilisateur',
        on_delete=models.CASCADE,
        related_name='mes_commentaires',
        help_text="L'identifiant à qui appartient ce commentaire"
    )

    texte = models.TextField(
        help_text="Le contenu du commentaire",
    )

    date_creation_commentaire = models.DateTimeField(
        auto_now_add=True,
        help_text="Date et Heure de création du commentaire"
    )

    commentaire_parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='reponses',
        help_text="Le commentaire parent"
    )

    masque = models.BooleanField(
        default=False, 
        help_text="Commentaire masqué par la modération"
    )

    

     # --- VALIDATION DES RÈGLES MÉTIER ---
    def clean(self):
        """
        Valide les règles métier :
        1. La réponse doit appartenir à la même randonnée que son parent
        2. Maximum 2 niveaux de réponses (commentaire → réponse → réponse à réponse)
        """
        super().clean()
        parent = self.commentaire_parent
        
        if parent is None:
            return

        if self.pk and parent.pk == self.pk:
            raise ValidationError({'commentaire_parent': "Un commentaire ne peut pas se répondre à lui-même."})
        
        # Règle 1 : Le parent doit être sur la même randonnée
        if parent.randonnee_id != self.randonnee_id:
            raise ValidationError({
                'commentaire_parent': "La réponse doit appartenir à la même randonnée que son parent."
            })
        
        # Règle 2 : Maximum 2 niveaux de profondeur
        # Si le parent a lui-même un parent qui a un parent, on est au 3ème niveau → refusé
        if parent.commentaire_parent and parent.commentaire_parent.commentaire_parent:
            raise ValidationError({
                'commentaire_parent': "Nombre maximal de niveaux de réponses atteint (2 niveaux max)."
            })


    class Meta:
        db_table = "commentaires"
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['date_creation_commentaire']

    def __str__(self) -> str:
        return f"{self.texte}"


class Like(models.Model):
    """Ce modèle gère les likes des utilisateurs sur une randonnée"""

    auteur = models.ForeignKey(
        'comptes.Utilisateur',
        on_delete=models.CASCADE,
        related_name='mes_likes',
        help_text="L'auteur de ce like"
    )

    randonnee = models.ForeignKey(
        'randonnees.Randonnee',
        on_delete=models.CASCADE,
        related_name='likes',
        help_text="Les randonnées likés"
    )

    date_du_like = models.DateTimeField(
        auto_now_add=True,
        help_text="La date à laquelle la randonnée a été likés"
    )


    class Meta:
        db_table = 'likes'
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        ordering = ["-date_du_like"]
        constraints = [
            models.UniqueConstraint(fields=['auteur', 'randonnee'], name='unique_like_par_utilisateur_et_randonnee')
        ]

    def __str__(self) -> str:
        return f"{self.date_du_like} - Date du like"



class Abonnement(models.Model):
    """Ce modèle gère les abonnement des utilisateurs"""

    abonne = models.ForeignKey(
        'comptes.Utilisateur',
        on_delete=models.CASCADE,
        related_name='abonnements',
        help_text="Celui qui suit "
    )

    suivi = models.ForeignKey(
        'comptes.Utilisateur',
        on_delete=models.CASCADE,
        related_name='abonnes',
        help_text="Celui qui est suivi"
    )

    date_abonnement = models.DateTimeField(
        auto_now_add=True,
        help_text="La date de l'abonnement"
    )


    class Meta:
        db_table = "abonnements"
        verbose_name = "Abonnement"
        verbose_name_plural = "Abonnements"
        ordering = ["-date_abonnement"]
        constraints = [
            models.UniqueConstraint(fields=['abonne', 'suivi'], name='unique_abonnement'),
            models.CheckConstraint(condition=~models.Q(abonne=models.F('suivi')),
            name='abonnement_pas_soi_meme'),
        ]

    def __str__(self) -> str:
        return f"{self.abonne} a commencé à suivre {self.suivi} depuis le {self.date_abonnement}"



class Blocage(models.Model):
    """Ce modèle gère les utilisateurs qui ont été bloqué par d'autre utilisateurs"""

    utilisateur_bloque = models.ForeignKey(
        'comptes.Utilisateur',
        on_delete=models.CASCADE,
        related_name='bloque_par',
        help_text="Celui qui est bloqué "
    )

    utilisateur = models.ForeignKey(
        'comptes.Utilisateur',
        on_delete=models.CASCADE,
        related_name='mes_blocages',
        help_text="Celui qui bloque"
    )

    date_compte_bloque = models.DateTimeField(
        auto_now_add=True,
        help_text="La date où le compte a été bloqué"
    )


    class Meta:
        db_table = "blocages"
        verbose_name = "Blocage"
        verbose_name_plural = "Blocages"
        ordering = ["-date_compte_bloque"]
        constraints = [
            models.UniqueConstraint(
            fields=['utilisateur_bloque', 'utilisateur'], name="unique_blocage"),
            models.CheckConstraint(condition=~models.Q(utilisateur=models.F('utilisateur_bloque')), name="blocage_pas_soi_meme"),
        ]

    def __str__(self) -> str:
        return f"{self.utilisateur} a bloqué {self.utilisateur_bloque} le {self.date_compte_bloque}"



class TypeDeSignalement(models.TextChoices):
    RANDONNEE = 'randonnee', 'Randonnée'
    UTILISATEUR = 'utilisateur', 'Utilisateur'
    COMMENTAIRE = 'commentaire', 'Commentaire'



class Signalement(models.Model):
    """Ce modèle gère les utilisateurs, les randonnées et les commentaires qui ont été signalés"""

    type_signalement = models.CharField(
        max_length=20, 
        choices=TypeDeSignalement.choices, 
        help_text="Signalé un commentaire, une randonnée ou un utilisateur "
    )

    type_signalement_id = models.PositiveIntegerField(
        help_text="L'ID du contenu signalé soit randonnée, utilisateur ou commentaire fais intensionellement"
    )


    signaleur = models.ForeignKey(
        'comptes.Utilisateur',
        on_delete=models.CASCADE,
        related_name='mes_signalements',
        help_text="L'utilisateur qui signale un autre utilisateur ou une randonnee ou un commentaire"
    )

    motif_signale = models.TextField(
        help_text="Quelle est la raison de ce signalement"
    )

    statut_signale = models.BooleanField(
        blank=True,
        default=False,
        help_text="Le statut du signalement est traité ou non traité"
    )

    date_signalement = models.DateTimeField(
        auto_now_add=True,
        help_text="La date où l'utilisateur ou la randonnee ou le commentaire ont été signalés"
    )


    class Meta:
        db_table = "signalements"
        verbose_name = "Signalement"
        verbose_name_plural = "Signalements"
        ordering = ["-date_signalement"]
        constraints = [
            models.UniqueConstraint(fields=[
                'type_signalement',
                'type_signalement_id', 
                'signaleur', 
            ], 
            name="unique_signalement_pour_commentaire_randonnee_utilisateur"
            )
        ]

    def __str__(self) -> str:
        return f"Signalé le {self.date_signalement}"
    
