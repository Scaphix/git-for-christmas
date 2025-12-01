from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import path
from .models import Match, GiftAssignment
from .views import generate_matches

# Register your models here.


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('giver', 'receiver', 'created_at')
    search_fields = ('giver__user__username', 'receiver__user__username')
    actions = ['generate_secret_santa_matches', 'clear_all_matches']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'generate-matches/',
                self.admin_site.admin_view(self.generate_matches_view),
                name='matches_match_generate',
            ),
            path(
                'clear-matches/',
                self.admin_site.admin_view(self.clear_matches_view),
                name='matches_match_clear',
            ),
        ]
        return custom_urls + urls

    @admin.action(description="🎅 Generate Secret Santa Matches")
    def generate_secret_santa_matches(self, request, queryset):
        """Admin action to generate matches for all participants."""
        # Clear existing matches and gift assignments first
        existing_match_count = Match.objects.count()
        existing_gift_count = GiftAssignment.objects.count()
        if existing_match_count > 0 or existing_gift_count > 0:
            GiftAssignment.objects.all().delete()
            Match.objects.all().delete()
            self.message_user(
                request,
                (
                    f"🗑️ Cleared {existing_match_count} existing match(es) "
                    f"and {existing_gift_count} gift assignment(s) first."
                ),
                level=messages.INFO
            )

        success, message = generate_matches()
        if success:
            self.message_user(
                request, f"✅ {message}", level=messages.SUCCESS
            )
        else:
            self.message_user(
                request, f"❌ {message}", level=messages.ERROR
            )

    @admin.action(description="🗑️ Clear All Matches")
    def clear_all_matches(self, request, queryset):
        """Admin action to delete all matches and gift assignments."""
        match_count = Match.objects.count()
        gift_count = GiftAssignment.objects.count()
        GiftAssignment.objects.all().delete()  # Delete assignments first
        Match.objects.all().delete()
        self.message_user(
            request,
            (
                f"✅ Successfully deleted {match_count} match(es) and "
                f"{gift_count} gift assignment(s)."
            ),
            level=messages.SUCCESS
        )

    def changelist_view(self, request, extra_context=None):
        """Add custom context for the change list template."""
        extra_context = extra_context or {}
        extra_context['matches_count'] = Match.objects.count()
        return super().changelist_view(
            request, extra_context
        )

    def generate_matches_view(self, request):
        """Custom admin view to generate matches."""
        # Clear existing matches and gift assignments first
        existing_match_count = Match.objects.count()
        existing_gift_count = GiftAssignment.objects.count()
        if existing_match_count > 0 or existing_gift_count > 0:
            GiftAssignment.objects.all().delete()
            Match.objects.all().delete()
            self.message_user(
                request,
                (
                    f"🗑️ Cleared {existing_match_count} existing match(es) "
                    f"and {existing_gift_count} gift assignment(s) first."
                ),
                level=messages.INFO
            )

        success, message = generate_matches()
        if success:
            self.message_user(
                request, f"✅ {message}", level=messages.SUCCESS
            )
        else:
            self.message_user(
                request, f"❌ {message}", level=messages.ERROR
            )

        return redirect('admin:matches_match_changelist')

    def clear_matches_view(self, request):
        """Custom admin view to clear all matches and gift assignments."""
        match_count = Match.objects.count()
        gift_count = GiftAssignment.objects.count()
        GiftAssignment.objects.all().delete()  # Delete assignments first
        Match.objects.all().delete()
        self.message_user(
            request,
            (
                f"✅ Deleted {match_count} match(es) and "
                f"{gift_count} gift assignment(s)."
            ),
            level=messages.SUCCESS
        )
        return redirect('admin:matches_match_changelist')
