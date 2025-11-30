from django.shortcuts import render
from .models import Match

# Create your views here.


def matches_list(request):
    """Show all gift wish list items."""
    matches = Match.objects.all().order_by("-created_at")

    context = {
        "matches": matches,
    }

    return render(request, "matches/matches_list.html", context)
