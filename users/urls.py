from django.urls import path
from . import views

urlpatterns = [
    path("", views.santas_list, name="santas_list"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("join/", views.join_secret_santa, name="join_secret_santa"),
]
