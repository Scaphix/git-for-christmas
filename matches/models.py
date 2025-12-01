from django.db import models
from users.models import Participant


class Match(models.Model):
    """
    Giver -> Receiver match result.
    This stores the final, generated Secret Santa pair.
    """
    giver = models.OneToOneField(
        Participant,
        on_delete=models.CASCADE,
        related_name='giving_to'
    )
    receiver = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name='receiving_from'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.giver.user.username} → {self.receiver.user.username}"

    class Meta:
        verbose_name_plural = "Matches"
