import django_filters

from .models import JobPosting


class JobPostingFilter(django_filters.FilterSet):
    """
    Filter set for the job postings list endpoint.

    All filters operate on public fields only. Premium fields are never
    exposed as filter targets to avoid leaking data through filter inference.

    Supported parameters:

        location        Case-insensitive exact match on the location field.
        location_in     Accepts a comma-separated list of locations and returns
                        postings that match any of the provided values.
        created_after   Returns postings created at or after the given datetime.
        created_before  Returns postings created at or before the given datetime.
    """

    location = django_filters.CharFilter(
        field_name="location",
        lookup_expr="iexact",
    )
    location_in = django_filters.BaseInFilter(
        field_name="location",
        lookup_expr="iexact",
    )
    created_after = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
    )
    created_before = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
    )

    class Meta:
        model = JobPosting
        fields = ["location", "location_in", "created_after", "created_before"]