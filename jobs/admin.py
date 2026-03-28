from django.contrib import admin

from .models import JobPosting


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    """
    Admin configuration for JobPosting.

    Premium fields (company_name, salary_range, application_link) are grouped
    separately to reinforce the distinction between public and restricted data.
    The is_active flag can be toggled directly from the list view to quickly
    deactivate postings without opening the detail form.
    """

    list_display = ["title", "company_name", "location", "is_active", "created_at"]
    list_filter = ["is_active", "location", "created_at"]
    list_editable = ["is_active"]
    search_fields = ["title", "description", "company_name"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (
            "Public information",
            {
                "fields": ("title", "description", "location", "is_active"),
            },
        ),
        (
            "Premium information",
            {
                "description": "These fields are masked for Basic and unauthenticated users.",
                "fields": ("company_name", "salary_range", "application_link"),
                "classes": ("collapse",),
            },
        ),
        (
            "Record metadata",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )