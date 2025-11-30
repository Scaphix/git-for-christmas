from django.db import models

# Create your models here.


class User(models.Model): 
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
class Player(models.Model):
    """
    Shows a player in the Secret Santa event. 
    The organizer inputs these names.
    """
    user_id = models.CharField(max_length=100, unique=True, primary_key=True, help_text="unique identifier assigned by the organizer for pairing purposes.")
    name = models.CharField(max_length=100, help_text="The participant's display name.")
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Player"
        verbose_name_plural = "Players"
