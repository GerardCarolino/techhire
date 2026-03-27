from django.contrib import admin
from .models import JobPosting


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ["title", "company_name", "location", "salary_range", "is_active", "created_at"]
    list_filter = ["is_active", "location", "created_at"]
    search_fields = ["title", "description", "company_name"]
    list_editable = ["is_active"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        ("Public Info", {
            "fields": ("title", "description", "location", "is_active"),
        }),
        ("Premium Info (masked for Basic users)", {
            "fields": ("company_name", "salary_range", "application_link"),
            "classes": ("collapse",),
        }),
        ("Metadata", {
            "fields": ("created_at", "updated_at"),
        }),
    )
