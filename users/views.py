from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Participant


def santas_list(request):
    """Show a list of all Santas registered for the Christmas gift exchange."""
    santas = Participant.objects.all().order_by("-created_at")

    context = {
        "santas": santas,
    }

    return render(request, "users/santas_list.html", context)


def login_view(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect('santas_list')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('santas_list')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


def register_view(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('santas_list')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a Participant for the new user
            Participant.objects.create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(
                request,
                f'Account created for {username}! You can now log in.'
            )
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})


def logout_view(request):
    """User logout view."""
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
    return redirect('santas_list')


@login_required
def join_secret_santa(request):
    """Allow logged-in users to join the Secret Santa event."""
    if request.user.is_authenticated:
        # Check if user already has a participant record
        participant, created = Participant.objects.get_or_create(
            user=request.user
        )
        
        if created:
            messages.success(
                request,
                f'Welcome to Secret Santa, {request.user.username}! 🎅'
            )
        else:
            messages.info(
                request,
                'You are already a participant! 🎄'
            )
    
    return redirect('santas_list')
