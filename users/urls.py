from django.urls import path
from django.shortcuts import render

from . import views  # import your views module from the same package

urlpatterns = [
    path("", views.santas_list, name="santas_list"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
]


def santas_list_view(request):
    """
    Renders the main Secret Santa list and matching interface.
    """
    return render(request, 'users/santas_list.html', {})
