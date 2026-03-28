from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import JobPosting
from .serializers import JobPostingSerializer
from .filters import JobPostingFilter


class JobPostingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only endpoint for browsing active job postings.

    List:   GET /api/jobs/
    Detail: GET /api/jobs/<id>/

    Authentication is optional. When a valid JWT is provided, the serializer
    inspects the caller's membership tier and reveals or masks the three
    premium fields accordingly. This view has no knowledge of that logic --
    masking is the serializer's responsibility.

    Supported query parameters:

        search          Full-text match against title and description.
        location        Exact location filter (case-insensitive).
        location_in     Comma-separated list of locations.
        created_after   ISO 8601 datetime lower bound on created_at.
        created_before  ISO 8601 datetime upper bound on created_at.
        ordering        Field to sort by. Prefix with "-" to reverse.
                        Accepted values: created_at, title.
                        Default: -created_at (newest first).
        page            Page number. Each page contains 10 results.
    """

    queryset = JobPosting.objects.filter(is_active=True).order_by("-created_at")
    serializer_class = JobPostingSerializer
    permission_classes = [permissions.AllowAny]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = JobPostingFilter
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "title"]
    ordering = ["-created_at"]