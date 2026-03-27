import django_filters
from .models import JobPosting


class JobPostingFilter(django_filters.FilterSet):
    """
    Filtering options for the /api/jobs/ endpoint.

    Query params
    ────────────
    location    – exact match (case-insensitive)     ?location=Remote
    location_in – comma-separated list               ?location_in=Remote,New York
    created_after  – jobs posted after date          ?created_after=2024-01-01
    created_before – jobs posted before date         ?created_before=2024-12-31
    """

    location = django_filters.CharFilter(
        field_name="location",
        lookup_expr="iexact",
        label="Filter by location (exact, case-insensitive)",
    )
    location_in = django_filters.BaseInFilter(
        field_name="location",
        lookup_expr="iexact",
        label="Filter by multiple locations (comma-separated)",
    )
    created_after = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
        label="Jobs posted after this date (ISO 8601)",
    )
    created_before = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
        label="Jobs posted before this date (ISO 8601)",
    )

    class Meta:
        model = JobPosting
        fields = ["location", "location_in", "created_after", "created_before"]
