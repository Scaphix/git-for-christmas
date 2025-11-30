from django.db import models

# Create your models here.

class Participant(models.Model):
    """
    registered user in the Secret Santa event.
    user_id is the primary identifier
    """
    user_id = models.CharField(max_length=100, unique=True, primary_key=True, help_text="unique ID from the frontend auth service.")
    name = models.CharField(max_length=100, help_text="The participant's display name.")
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Participant"
        verbose_name_plural = "Participants"


class Match(models.Model):
    """
    Represents a single Giver -> Recipient match result.
    This stores the final, generated pairs.
    """
    # person giving the gift
    giver = models.one_to_one_field(Participant, related_name='giving_match', on_delete=models.CASCADE)
    
    # person receiving the gift
    recipient = models.one_to_one_field(Participant, related_name='receiving_match', on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.giver.name} -> {self.recipient.name}"

    class Meta:
        verbose_name_plural = "Matches"
        # ensure no giver is matched twice
        constraints = [
            models.UniqueConstraint(fields=['giver'], name='unique_giver'),
            models.UniqueConstraint(fields=['recipient'], name='unique_recipient'),
        ]
