from django.urls import path
from django.shortcuts import render

from . import views  # import your views module from the same package

urlpatterns = [
    path("", views.home, name="home"),
    path("santas/", views.santas_list, name="santas_list"),
]


def santas_list_view(request):
    """
    Renders the main Secret Santa list and matching interface.
    """
    return render(request, 'users/santas_list.html', {})
