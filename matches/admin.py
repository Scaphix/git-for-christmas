from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import path
from django.utils.html import format_html
from .models import Match
from .views import generate_matches

# Register your models here.


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('giver', 'receiver', 'created_at', 'match_actions')
    search_fields = ('giver__user__username', 'receiver__user__username')

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

    def match_actions(self, obj):
        """Display action buttons in list view."""
        generate_url = "/admin/matches/match/generate-matches/"
        clear_url = "/admin/matches/match/clear-matches/"
        generate_style = (
            "background-color: #417690; color: white; "
            "padding: 10px 15px; text-decoration: none; "
            "border-radius: 4px; margin-right: 10px;"
        )
        clear_style = (
            "background-color: #ba2121; color: white; "
            "padding: 10px 15px; text-decoration: none; "
            "border-radius: 4px;"
        )
        return format_html(
            '<a class="button" href="{}" style="{}">'
            '🎅 Generate Matches</a> '
            '<a class="button" href="{}" style="{}">'
            '🗑️ Clear All</a>',
            generate_url, generate_style, clear_url, clear_style
        )
    match_actions.short_description = 'Actions'

    def generate_matches_view(self, request):
        """Custom admin view to generate matches."""
        if Match.objects.exists():
            self.message_user(
                request,
                "⚠️ Matches already exist! Clear them first.",
                level=messages.WARNING
            )
        else:
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
