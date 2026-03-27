from rest_framework import serializers
from .models import JobPosting

LOCKED = "🔒 Premium Feature"


class JobPostingSerializer(serializers.ModelSerializer):
    """
    Serializer with field-level masking for premium-only fields.

    How it works
    ────────────
    The serializer receives the DRF Request object via context
    (automatically injected by ModelViewSet).  In `to_representation`
    we inspect whether the requesting user is authenticated AND has a
    Premium membership tier.  If not, the three sensitive fields are
    replaced with the LOCKED sentinel string before the data leaves
    the API.

    Premium fields: company_name · salary_range · application_link
    """

    PREMIUM_FIELDS = ("company_name", "salary_range", "application_link")

    class Meta:
        model = JobPosting
        fields = [
            "id",
            "title",
            "description",
            "location",
            # ↓ these three will be masked for non-premium users
            "company_name",
            "salary_range",
            "application_link",
            "created_at",
        ]

    # ── Helper ────────────────────────────────────────────────────────────────

    def _is_premium_user(self) -> bool:
        """
        Returns True only when:
          1. A valid JWT was provided (request.user is authenticated), AND
          2. The associated UserProfile has membership_tier == "premium".
        """
        request = self.context.get("request")

        # No request context (e.g. admin serializer usage) → treat as basic
        if request is None:
            return False

        user = request.user

        # AnonymousUser or failed JWT validation
        if not user or not user.is_authenticated:
            return False

        # Guard against users without a profile (shouldn't happen, but safe)
        profile = getattr(user, "profile", None)
        if profile is None:
            return False

        return profile.is_premium

    # ── Masking ───────────────────────────────────────────────────────────────

    def to_representation(self, instance):
        """Intercept the default representation and mask premium fields."""
        data = super().to_representation(instance)

        if not self._is_premium_user():
            for field in self.PREMIUM_FIELDS:
                data[field] = LOCKED

        return data
