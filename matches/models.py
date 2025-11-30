from django.db import models
from users.models import Participant

# Create your models here.


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
