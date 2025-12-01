from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Participant

# Create your views here.


# adding this view to avoid error since someone added this inside url file
def home(request):
    """
    Placeholder view required by the 'users' app URL configuration.
    """
    return JsonResponse({'status': 'ok', 'message': 'User app base path is active.'})


def santas_list(request):
    """
    Placeholder view required by the existing 'users' app URL configuration 
    for the /santas/ path.
    """
    return JsonResponse({'status': 'ok', 'message': 'Santas list view is active.'})
    # Show a list of all Santas registered for the Christmas gift exchange.
    santas = Participant.objects.all().order_by("-created_at")


    return render(request, "users/santas_list.html", context)
