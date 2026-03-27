from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import JobPosting
from .serializers import JobPostingSerializer
from .filters import JobPostingFilter


class JobPostingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    /api/jobs/        – list all active job postings
    /api/jobs/<id>/   – retrieve a single job posting

    Authentication is optional. The serializer applies field-level masking
    automatically based on the caller's membership tier:

      • No token  →  premium fields masked
      • Basic JWT →  premium fields masked
      • Premium JWT →  full data returned

    Search & Filter
    ───────────────
    ?search=<text>         searches title + description (case-insensitive)
    ?location=<city>       filter by exact location
    ?location_in=A,B,C     filter by multiple locations
    ?created_after=<date>  filter by date (ISO 8601)
    ?created_before=<date> filter by date (ISO 8601)
    ?ordering=created_at   change ordering (default: -created_at, newest first)
    ?page=<n>              page number (10 results per page)
    """

    queryset = JobPosting.objects.filter(is_active=True).order_by("-created_at")
    serializer_class = JobPostingSerializer
    permission_classes = [permissions.AllowAny]

    # ── Search, filter, ordering ──────────────────────────────────────────────
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = JobPostingFilter
    search_fields = ["title", "description"]          # ?search=
    ordering_fields = ["created_at", "title"]         # ?ordering=
    ordering = ["-created_at"]                        # default: newest first
