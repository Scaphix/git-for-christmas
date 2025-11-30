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
    Simple function to match participants in pairs.
    User 1 → User 2, User 3 → User 4, etc.
    If odd number, last user is unmatched.

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

            # Match in pairs: person 0 → person 1, person 2 → person 3, etc.
            matches_created = 0
            for i in range(0, len(participants), 2):
                # If odd number, skip the last person
                if i + 1 >= len(participants):
                    break

                giver = participants[i]
                receiver = participants[i + 1]
                Match.objects.create(giver=giver, receiver=receiver)
                matches_created += 1

            # Check if someone was left unmatched
            unmatched = len(participants) % 2
            if unmatched:
                msg = (f"Successfully matched {matches_created} pair(s)! "
                       f"1 participant left unmatched (odd number).")
            else:
                msg = f"Successfully matched {matches_created} pair(s)!"

            return True, msg

    except Exception as e:
        return False, f"Error: {str(e)}"
