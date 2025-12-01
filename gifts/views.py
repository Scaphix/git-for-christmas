from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import WishListItem
from .forms import WishListItemForm
from users.models import Participant


def gifts_list(request):
    """Show all gift wish list items."""
    gifts = WishListItem.objects.all().order_by("-created_at")

    context = {
        "gifts": gifts,
    }

    return render(request, "gifts/gifts_list.html", context)


@login_required
def add_wishlist_item(request):
    """Allow authenticated users to add a wishlist item."""
    # Get or create participant for the user
    participant, created = Participant.objects.get_or_create(
        user=request.user
    )
    
    if created:
        messages.info(
            request,
            'Participant profile created automatically. You can now add wishlist items!'
        )

    if request.method == 'POST':
        form = WishListItemForm(request.POST)
        if form.is_valid():
            wishlist_item = form.save(commit=False)
            wishlist_item.participant = participant
            wishlist_item.save()
            messages.success(request, 'Wishlist item added successfully!')
            return redirect('gifts_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = WishListItemForm()

    context = {
        'form': form,
    }
    return render(request, 'gifts/add_wishlist_item.html', context)


@login_required
def edit_wishlist_item(request, item_id):
    """Allow users to edit their own wishlist items."""
    # Get or create participant for the user
    participant, created = Participant.objects.get_or_create(
        user=request.user
    )
    
    if created:
        messages.info(
            request,
            'Participant profile created automatically.'
        )

    wishlist_item = get_object_or_404(WishListItem, id=item_id)

    # Check if the user owns this item
    if wishlist_item.participant.user != request.user:
        messages.error(request, 'You can only edit your own wishlist items.')
        return redirect('gifts_list')

    if request.method == 'POST':
        form = WishListItemForm(request.POST, instance=wishlist_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Wishlist item updated successfully!')
            return redirect('gifts_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = WishListItemForm(instance=wishlist_item)

    context = {
        'form': form,
        'item': wishlist_item,
    }
    return render(request, 'gifts/edit_wishlist_item.html', context)


@login_required
def delete_wishlist_item(request, item_id):
    """Allow users to delete their own wishlist items."""
    wishlist_item = get_object_or_404(WishListItem, id=item_id)

    # Check if the user owns this item
    if wishlist_item.participant.user != request.user:
        messages.error(request, 'You can only delete your own wishlist items.')
        return redirect('gifts_list')

    if request.method == 'POST':
        item_title = wishlist_item.title
        wishlist_item.delete()
        messages.success(
            request,
            f'Wishlist item "{item_title}" deleted successfully!'
        )
        return redirect('gifts_list')

    context = {
        'item': wishlist_item,
    }
    return render(request, 'gifts/delete_wishlist_item.html', context)
