from django.shortcuts import render
from .models import Participant
# Create your views here.


def santas_list(request):
    # Show a list of all Santas registered for the Christmas gift exchange.
    santas = Participant.objects.all().order_by("-created_at")

    context = {
        "santas": santas,
    }

    return render(request, "users/santas_list.html", context)
