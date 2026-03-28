from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserProfile.

    Displays membership tier alongside the associated username so staff can
    quickly identify and manage user access levels without opening each record.
    """

    list_display = ["user", "membership_tier", "created_at"]
    list_filter = ["membership_tier"]
    search_fields = ["user__username", "user__email"]
    raw_id_fields = ["user"]
    readonly_fields = ["created_at", "updated_at"]