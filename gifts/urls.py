from django.urls import path
from . import views  # import your views module from the same package

urlpatterns = [
    path("", views.gifts_list, name="gifts_list"),
]
