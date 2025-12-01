from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import path
from .models import WishListItem
from matches.views import assign_gifts_to_matches, clear_gift_assignments
from matches.models import GiftAssignment

# Register your models here.


@admin.register(WishListItem)
class WishListItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'participant', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'participant__user__username')
    actions = ['assign_gifts_to_matches', 'clear_all_gift_assignments']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'assign-gifts/',
                self.admin_site.admin_view(self.assign_gifts_view),
                name='gifts_wishlistitem_assign_gifts',
            ),
            path(
                'clear-gifts/',
                self.admin_site.admin_view(self.clear_gifts_view),
                name='gifts_wishlistitem_clear_gifts',
            ),
        ]
        return custom_urls + urls

    @admin.action(description="🎁 Assign Gifts to Matches")
    def assign_gifts_to_matches(self, request, queryset):
        """Admin action to assign gifts to existing matches."""
        success, message = assign_gifts_to_matches()
        if success:
            self.message_user(
                request, f"✅ {message}", level=messages.SUCCESS
            )
        else:
            self.message_user(
                request, f"❌ {message}", level=messages.ERROR
            )

    @admin.action(description="🗑️ Clear All Gift Assignments")
    def clear_all_gift_assignments(self, request, queryset):
        """Admin action to clear all gift assignments."""
        success, message = clear_gift_assignments()
        if success:
            self.message_user(
                request, f"✅ {message}", level=messages.SUCCESS
            )
        else:
            self.message_user(
                request, f"❌ {message}", level=messages.ERROR
            )

    def changelist_view(self, request, extra_context=None):
        """Add custom context for the change list template."""
        extra_context = extra_context or {}
        extra_context['gift_assignments_count'] = (
            GiftAssignment.objects.count()
        )
        return super().changelist_view(request, extra_context)

    def assign_gifts_view(self, request):
        """Custom admin view to assign gifts to matches."""
        success, message = assign_gifts_to_matches()
        if success:
            self.message_user(
                request, f"✅ {message}", level=messages.SUCCESS
            )
        else:
            self.message_user(
                request, f"❌ {message}", level=messages.ERROR
            )
        return redirect('admin:gifts_wishlistitem_changelist')

    def clear_gifts_view(self, request):
        """Custom admin view to clear all gift assignments."""
        success, message = clear_gift_assignments()
        if success:
            self.message_user(
                request, f"✅ {message}", level=messages.SUCCESS
            )
        else:
            self.message_user(
                request, f"❌ {message}", level=messages.ERROR
            )
        return redirect('admin:gifts_wishlistitem_changelist')
