from django.db import models
from users.models import Participant

# Create your models here.


class WishListItem(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.participant.user.username}"
