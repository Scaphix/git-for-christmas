from django.shortcuts import render
from .models import User
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