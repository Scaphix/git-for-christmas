import random
from django.shortcuts import render
from django.db import transaction
from .models import Match
from users.models import Participant


def matches_list(request):
    """Show all Secret Santa matches."""
    matches = Match.objects.all().order_by("-created_at")

    context = {
        "matches": matches,
    }

    return render(request, "matches/matches_list.html", context)


def generate_matches():
    """
    Randomly match each participant with another participant.
    Each person gives to a randomly assigned person (circular matching).

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
            random.shuffle(participants)

            # Create circular random matches
            # Each person gives to the next person in the shuffled list
            # Last person gives to first person (ensures everyone is matched)
            for i in range(len(participants)):
                giver = participants[i]
                receiver = participants[(i + 1) % len(participants)]
                Match.objects.create(giver=giver, receiver=receiver)

            count = len(participants)
            return True, f"Successfully matched {count} participants!"

    except Exception as e:
        return False, f"Error: {str(e)}"
