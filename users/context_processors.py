from .models import Participant


def participant_status(request):
    """
    Context processor to add participant status to all templates.
    Makes it easy to distinguish between authenticated users and participants.
    """
    is_participant = False
    participant = None
    
    if request.user.is_authenticated:
        try:
            participant = Participant.objects.get(user=request.user)
            is_participant = True
        except Participant.DoesNotExist:
            is_participant = False
    
    return {
        'is_participant': is_participant,
        'user_participant': participant,
    }

