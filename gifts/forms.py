from django import forms
from .models import WishListItem


class WishListItemForm(forms.ModelForm):
    """Form for creating and editing wishlist items."""
    
    class Meta:
        model = WishListItem
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter gift title...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter gift description (optional)...'
            }),
        }
        labels = {
            'title': 'Gift Title',
            'description': 'Description (Optional)',
        }

