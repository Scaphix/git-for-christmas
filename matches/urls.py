from django.urls import path
from . import views  # import your views module from the same package

urlpatterns = [
    path("", views.matches_list, name="matches_list"),
]
