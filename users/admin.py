from django.contrib import admin
from django.contrib import messages
from django import forms
from .models import Participant

# Register your models here.


class ParticipantAdminForm(forms.ModelForm):
    """Custom form that prevents creating new Users from Participant admin."""
    
    class Meta:
        model = Participant
        fields = '__all__'
        widgets = {
            'user': forms.Select(attrs={'style': 'width: 300px;'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show users that don't already have a participant
        if self.instance and self.instance.pk:
            # Editing existing participant - show all users
            self.fields['user'].queryset = self.fields['user'].queryset.all()
        else:
            # Adding new participant - only show users without participants
            from django.contrib.auth.models import User
            existing_participant_user_ids = Participant.objects.values_list('user_id', flat=True)
            self.fields['user'].queryset = User.objects.exclude(
                id__in=existing_participant_user_ids
            )


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    form = ParticipantAdminForm
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)
    actions = ['delete_selected_participants']
    
    @admin.action(description="🗑️ Delete selected participants")
    def delete_selected_participants(self, request, queryset):
        """Custom delete action with confirmation message."""
        count = queryset.count()
        queryset.delete()
        self.message_user(
            request,
            f"✅ Successfully deleted {count} participant(s).",
            level=messages.SUCCESS
        )
    
    def get_form(self, request, obj=None, **kwargs):
        """Override form to disable add button on user field."""
        form = super().get_form(request, obj, **kwargs)
        user_field = form.base_fields.get('user')
        if user_field:
            # Disable the add button - this works for AdminForeignKeyWidget
            if hasattr(user_field.widget, 'can_add_related'):
                user_field.widget.can_add_related = False
            # For nested widgets
            if hasattr(user_field.widget, 'widget'):
                if hasattr(user_field.widget.widget, 'can_add_related'):
                    user_field.widget.widget.can_add_related = False
        return form
