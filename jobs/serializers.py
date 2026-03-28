from rest_framework import serializers
from .models import JobPosting

# Sentinel value returned in place of restricted fields.
# A plain string (no emoji) keeps the response machine-readable and allows
# frontend clients to detect masking with a simple equality check.
MASKED_VALUE = "[Premium]"


class JobPostingSerializer(serializers.ModelSerializer):
    """
    Serializer for JobPosting with field-level access control.

    Three fields are restricted to Premium members:
        company_name, salary_range, application_link

    The masking decision is made in `to_representation`, which runs once per
    object before the data is sent to the client. Non-premium callers receive
    the sentinel string MASKED_VALUE in place of each restricted field.

    Access tiers:
        Anonymous (no JWT)  -- all three fields masked
        Basic (valid JWT)   -- all three fields masked
        Premium (valid JWT) -- all three fields returned in full
    """

    PREMIUM_FIELDS = ("company_name", "salary_range", "application_link")

    class Meta:
        model = JobPosting
        fields = [
            "id",
            "title",
            "description",
            "location",
            "company_name",
            "salary_range",
            "application_link",
            "created_at",
        ]

    def _caller_has_premium_access(self) -> bool:
        """
        Returns True when the request carries a valid JWT belonging to a
        Premium-tier user. Returns False in all other cases, including:
            - No request context (e.g. shell/admin usage)
            - Anonymous or unauthenticated request
            - Authenticated Basic-tier user
            - User with no associated profile record
        """
        request = self.context.get("request")

        if request is None:
            return False

        user = request.user

        if not user or not user.is_authenticated:
            return False

        profile = getattr(user, "profile", None)

        if profile is None:
            return False

        return profile.is_premium

    def to_representation(self, instance):
        """
        Applies field-level masking before the serialized data is returned.

        Called automatically by DRF for every object in list and detail
        responses. The masking happens here rather than at the model or view
        layer to keep each layer responsible for a single concern.
        """
        data = super().to_representation(instance)

        if not self._caller_has_premium_access():
            for field in self.PREMIUM_FIELDS:
                data[field] = MASKED_VALUE

        return data