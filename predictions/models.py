from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Prediction(models.Model):
    """Ce modèle stocke les prédictions (fourchettes) générées par le modèle IA pour une randonnée."""

    POURCENTAGE_VALIDATORS = [MinValueValidator(0), MaxValueValidator(100)]

    # --- Relation 1 pour 1 avec la Randonnée ---
    randonnee = models.ForeignKey(
        'randonnees.Randonnee',
        on_delete=models.CASCADE,
        related_name='predictions',
        help_text="La randonnée associée à cette prédiction"
    )

    # --- Fourchettes de prédiction pour les VUES (nombres bruts) ---
    vues_min = models.IntegerField(
        default=0,
        help_text="Estimation minimale du nombre de vues (nombre brut)"
    )
    vues_max = models.IntegerField(
        default=0,
        help_text="Estimation maximale du nombre de vues (nombre brut)"
    )

    # --- Fourchettes de prédiction pour les LIKES (en POURCENTAGE) ---
    taux_likes_min = models.IntegerField(
        default=0,
        validators=POURCENTAGE_VALIDATORS,
        help_text="Taux de likes minimal en pourcentage (ex: 5 pour 5%)"
    )
    taux_likes_max = models.IntegerField(
        default=0,
        validators=POURCENTAGE_VALIDATORS,
        help_text="Taux de likes maximal en pourcentage (ex: 10 pour 10%)"
    )

    # --- Fourchettes de prédiction pour les COMMENTAIRES (en POURCENTAGE) ---
    taux_commentaires_min = models.IntegerField(
        default=0,
        validators=POURCENTAGE_VALIDATORS,
        help_text="Taux de commentaires minimal en pourcentage (4e variable prédite)"
    )
    taux_commentaires_max = models.IntegerField(
        default=0,
        validators=POURCENTAGE_VALIDATORS,
        help_text="Taux de commentaires maximal en pourcentage (4e variable prédite)"
    )

    # --- Fourchettes de prédiction pour les ABONNÉS GAGNÉS (nombres bruts) ---
    abonnes_min = models.IntegerField(
        default=0,
        help_text="Estimation minimale du nombre d'abonnés gagnés (nombre brut)"
    )
    abonnes_max = models.IntegerField(
        default=0,
        help_text="Estimation maximale du nombre d'abonnés gagnés (nombre brut)"
    )

    # --- Métadonnées du modèle IA ---
    version_modele = models.CharField(
        max_length=20,
        default="v1.0",
        help_text="Version du modèle IA utilisé pour générer cette prédiction"
    )

    # --- Dates ---
    date_creation = models.DateTimeField(
        auto_now_add=True,
        help_text="Date et heure de la génération de la prédiction"
    )

    class Meta:
        db_table = "predictions"
        verbose_name = "Prédiction"
        verbose_name_plural = "Prédictions"
        ordering = ["-date_creation"]

    def __str__(self) -> str:
        return f"Prédiction ({self.version_modele}) pour : {self.randonnee.titre_randonnee}"