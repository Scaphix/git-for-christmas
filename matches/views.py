import random
from django.shortcuts import render
from django.db import transaction
from .models import Match
from users.models import Participant

# Create your views here.


def matches_list(request):
    """Show all gift wish list items."""
    matches = Match.objects.all().order_by("-created_at")

    context = {
        "matches": matches,
    }

    return render(request, "matches/matches_list.html", context)


def generate_matches():
    """
    Simple function to match each participant with another.
    Creates circular matching: person 1 → person 2 → person 3 → ... → person 1
    
    Returns: (success: bool, message: str)
    """
    # Get all participants
    participants = list(Participant.objects.all())
    
    # Need at least 2 people
    if len(participants) < 2:
        return False, "Need at least 2 participants to create matches!"
    
    # Check if matches already exist
    if Match.objects.exists():
        return False, "Matches already exist! Clear them first."
    
    try:
        with transaction.atomic():
            # Shuffle participants randomly
            shuffled = participants.copy()
            random.shuffle(shuffled)
            
            # Create circular matches
            # Person at index i gives to person at index i+1
            # Last person gives to first person
            for i in range(len(shuffled)):
                giver = shuffled[i]
                receiver = shuffled[(i + 1) % len(shuffled)]
                
                # Create the match
                Match.objects.create(giver=giver, receiver=receiver)
            
            return True, f"Successfully matched {len(shuffled)} participants!"
            
    except Exception as e:
        return False, f"Error: {str(e)}"
