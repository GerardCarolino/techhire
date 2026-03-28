from django.db import models


class JobPosting(models.Model):
    """
    Represents a single job listing on the TechHire board.

    Fields are split into two access tiers:

    Public (visible to all callers):
        title, description, location

    Premium (masked for Basic and unauthenticated callers):
        company_name, salary_range, application_link

    Masking is enforced at the serializer layer, not here. The model
    holds the canonical data regardless of who is requesting it.
    """

    # Public fields -- returned to every caller
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)

    # Premium fields -- masked by JobPostingSerializer for non-premium callers
    company_name = models.CharField(max_length=200)
    salary_range = models.CharField(
        max_length=100,
        help_text='Formatted salary band, e.g. "$120,000 - $160,000".',
    )
    application_link = models.URLField(max_length=500)

    # Metadata
    is_active = models.BooleanField(
        default=True,
        help_text="Inactive postings are excluded from all API responses.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Job Posting"
        verbose_name_plural = "Job Postings"

    def __str__(self) -> str:
        return f"{self.title} at {self.company_name}"