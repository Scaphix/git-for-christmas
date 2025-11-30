from django.contrib import admin
from .models import Match

# Register your models here.


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('giver', 'receiver', 'created_at')
    search_fields = ('giver__user__username', 'receiver__user__username')
