from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from users.models import Player
from .models import Match
import json
import random

# Create your views here.

def generate_secret_santa_matches(players):
    """
    function to generate pairings that no one gives a gift to themselves.
    Fisher-Yates shuffle method for random, guaranteed pairings.
    """
    givers = list(players)
    recipients = list(players)
    
    # Shuffle the recipient list randomly
    random.shuffle(recipients)
    
    # The list of pairings to be returned
    matches = []
    
    # If a self-match occurs (A->A, re-shuffle until its fixed
    while any(givers[i] == recipients[i] for i in range(len(givers))):
        random.shuffle(recipients)
        
    # final match tuples 
    for giver, recipient in zip(givers, recipients):
        matches.append((giver, recipient))
        
    return matches


# --- API Endpoint ---

@csrf_exempt
def register_player(request):
    """
    API to add a new player to the pool
    Organizer uses this multiple times to input players name
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests allowed'}, status=405)

    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        name = data.get('name')
        
        if not user_id or not name:
            return JsonResponse({'error': 'Missing user_id or name'}, status=400)
        
        # Check if player already exists
        if Player.objects.filter(user_id=user_id).exists():
            return JsonResponse({'message': 'Player already registered'}, status=200)

        # Create the new player in the database
        player = Player.objects.create(user_id=user_id, name=name)
        
        return JsonResponse({'status': 'success', 'message': f'Player {name} registered.'})
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)


@csrf_exempt
def run_matching_logic(request):
    """
    API endpoint to initiate the Secret Santa matching process.
    It deletes any previous matches before running a new one.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests allowed'}, status=405)

    try:
        # Check if there are enough players
        players = list(Player.objects.all())
        if len(players) < 2:
            return JsonResponse({'error': 'Need at least two players to run the match.'}, status=400)
        
        with transaction.atomic():
            # Delete all existing matches to start fresh
            Match.objects.all().delete()
            
            # Generate the random pairings
            pairings = generate_secret_santa_matches(players)
            
            # Save the new matches to the database
            match_objects = [
                Match(giver=giver, recipient=recipient)
                for giver, recipient in pairings
            ]
            Match.objects.bulk_create(match_objects)
            
        return JsonResponse({'status': 'success', 'message': f'Matching complete! {len(pairings)} pairs created.'})
        
    except Exception as e:
        # Delete any partial matches if the save failed
        Match.objects.all().delete()
        return JsonResponse({'error': f'Matching failed: {str(e)}'}, status=500)


@csrf_exempt
def get_user_match(request):
    """
    API to retrieve the name of the recipient for a specific user ID (the Giver).
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET requests allowed'}, status=405)
    
    user_id = request.GET.get('user_id')
    
    if not user_id:
        return JsonResponse({'error': 'Missing user_id parameter'}, status=400)
        
    try:
        # Find the player object that matches the requested user_id
        giver_player = Player.objects.get(user_id=user_id)
        
        # Look up the match where this player is the giver
        match = Match.objects.get(giver=giver_player)
        
        # Return the recipient's name
        return JsonResponse({
            'status': 'success', 
            'giver_name': giver_player.name,
            'recipient_name': match.recipient.name, 
            'message': 'Match found.'
        })

    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Match or Player not found for this user_id. Did the match run yet?'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)


@csrf_exempt
def get_players(request):
    """
    API to return the list of all registered players
    Useful for organizer to check the list before running the match
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET requests allowed'}, status=405)
    
    try:
        players = Player.objects.all().values('user_id', 'name', 'registered_at')
        player_list = list(players)
        
        return JsonResponse({
            'status': 'success',
            'count': len(player_list),
            'players': player_list
        })
    except Exception as e:
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)
from .models import Match

# Create your views here.


def matches_list(request):
    """Show all gift wish list items."""
    matches = Match.objects.all().order_by("-created_at")

    context = {
        "matches": matches,
    }

    return render(request, "matches/matches_list.html", context)
