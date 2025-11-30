from django.db import models
from users.models import Participant

# Create your models here.

from users.models import Player 


class Match(models.Model):
    """
    Giver -> Recipient match result.
    This stores the final, generated Secret Santa pair
    """
    # the person giving the gift
    giver = models.OneToOneField(Player, related_name='giving_match', on_delete=models.CASCADE)
    
    # The person receiving the gift
    recipient = models.OneToOneField(Player, related_name='receiving_match', on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.giver.name} -> {self.recipient.name}"

    class Meta:
        verbose_name_plural = "Matches"
        # ensure no one gives or receives more than once
        constraints = [
            models.UniqueConstraint(fields=['giver'], name='unique_giver'),
            models.UniqueConstraint(fields=['recipient'], name='unique_recipient'),
        ]

class Match(models.Model):
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

