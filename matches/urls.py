from django.urls import path
from . import views

urlpatterns = [
    path("", views.matches_list, name="matches_list"),
]
