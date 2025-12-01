from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import path
from .models import Match
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
        # Clear existing matches first to prevent duplicates
        existing_count = Match.objects.count()
        if existing_count > 0:
            Match.objects.all().delete()
            self.message_user(
                request,
                f"🗑️ Cleared {existing_count} existing match(es) first.",
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
        """Admin action to delete all existing matches."""
        count = Match.objects.count()
        Match.objects.all().delete()
        self.message_user(
            request,
            f"✅ Successfully deleted {count} match(es).",
            level=messages.SUCCESS
        )

    def changelist_view(self, request, extra_context=None):
        """Add custom context for the change list template."""
        extra_context = extra_context or {}
        extra_context['matches_count'] = Match.objects.count()
        return super().changelist_view(request, extra_context)

    def generate_matches_view(self, request):
        """Custom admin view to generate matches."""
        # Clear existing matches first to prevent duplicates
        existing_count = Match.objects.count()
        if existing_count > 0:
            Match.objects.all().delete()
            self.message_user(
                request,
                f"🗑️ Cleared {existing_count} existing match(es) first.",
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
        """Custom admin view to clear all matches."""
        count = Match.objects.count()
        Match.objects.all().delete()
        self.message_user(
            request,
            f"✅ Deleted {count} match(es).",
            level=messages.SUCCESS
        )
        return redirect('admin:matches_match_changelist')
