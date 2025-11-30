from django.shortcuts import render
from .models import WishListItem

# Create your views here.


def gifts_list(request):
    """Show all gift wish list items."""
    gifts = WishListItem.objects.all().order_by("-created_at")

    context = {
        "gifts": gifts,
    }

    return render(request, "gifts/gifts_list.html", context)
