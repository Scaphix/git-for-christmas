from django.contrib import admin
from .models import WishListItem

# Register your models here.


@admin.register(WishListItem)
class WishListItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'participant', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'participant__user__username')
