from django.urls import path
from . import views

urlpatterns = [
    # API to register a new player 
    path('register/', views.register_player, name='register_player'),
    
    # API to get the current list of players 
    path('players/', views.get_players, name='get_players'),
    
    # 3. API to run the matching 
    path('run/', views.run_matching_logic, name='run_matching'),
    
    # 4. API to look up a player's assigned match
    path('lookup/', views.get_user_match, name='get_user_match'),
]
=======
from . import views  # import your views module from the same package

urlpatterns = [
    path("", views.matches_list, name="matches_list"),
]
